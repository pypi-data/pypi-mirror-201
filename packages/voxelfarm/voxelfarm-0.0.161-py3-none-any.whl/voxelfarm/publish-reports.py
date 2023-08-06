import pandas as pd
import time
from azure.eventhub import EventHubProducerClient, EventData
import json
import datetime
import glob
import os
from voxelfarm import process_lambda
from voxelfarm import workflow_lambda

lambda_host = process_lambda.process_lambda_host()
lambda_host.log('Starting publish reports...')

workflow_host = workflow_lambda.workflow_lambda_host()

scrap_folder= lambda_host.get_scrap_folder()
lambda_host.log('scrap_folder: ' + scrap_folder)
tools = lambda_host.get_tools_folder()
lambda_host.log('tools ' + tools)

raw_entityId = lambda_host.input_string('raw_entity_id', 'raw_entity', '')
timestampId = lambda_host.input_string('timestamp_id', 'timestampId', '')
spatialId = lambda_host.input_string('spatial_id', 'spatialId', '')
objectId = lambda_host.input_string('object_id', 'objectId', '')
defaultObjectId = lambda_host.input_string('default_object_id', 'defaultobjectId', '')
propertyStr = lambda_host.input_string('property_ids', 'propertyIds', '')
vf_ts_conn_str = lambda_host.input_string('vf_ts_conn_str', 'vf_ts_conn_str', '')
vf_ts_hub_name = lambda_host.input_string('vf_ts_hub_name', 'vf_ts_hub_name','')
timestamp = lambda_host.input_string('timestamp', 'timestamp', None)
constant_spatial_id = lambda_host.input_string('constant_spatial_id', 'constant_spatial_id', '')
constant_object_id = lambda_host.input_string('constant_object_id', 'constant_object_id', '')

arr = propertyStr.split('|')
propertyIds = []
for value in arr:
    if value != '':
        propertyIds.append(tuple(value.split(',')))

lambda_host.log(f'timestamp:{timestamp}|timestamp_id:{timestampId}|spatialId:{spatialId}|objectId:{objectId}|constant_spatial_id:{constant_spatial_id}|constant_object_id:{constant_object_id}')
lambda_host.log(f'propertyIds:{propertyIds}')

def is_number(element) -> bool:
    try:
        float(element)
        return True
    except:
        return False

def exit_code(code):
    lambda_host.set_exit_code(code)
    exit()

if not raw_entityId:
    lambda_host.log('Error Raw Entity not found')
    exit_code(1)

def submit_time_series_events(events:dict):
    lambda_host.log(f'Submit Timeseries events...')
    lambda_host.log(f'Creating producer Client...')
    if (len(events) == 0):
        lambda_host.log(f'Events are empty, exiting  function...')
        return { "success": True}
    lambda_host.log(f'Number of Events:{len(events)}')
    lambda_host.log(f'vf_ts_hub_name:{vf_ts_hub_name}')

    client =  EventHubProducerClient.from_connection_string(conn_str=vf_ts_conn_str, eventhub_name=vf_ts_hub_name)
    lambda_host.log('Creating a batch...')  
    event_data_batch = client.create_batch()
    lambda_host.log('Created a batch...')  
    # Add events to the batch.
    progressPercent = 0
    progessSentToHost = 0
    numEventsSent = 0
    i = 0
    can_add = True
    while (i < len(events)):
        try:
            event = events[i]
            eventStr = json.dumps(event)
            #lambda_host.log(f'adding {eventStr}')s
            event_data_batch.add(EventData(eventStr))
        except ValueError:
            can_add = False
        
        if (can_add) :
            #lambda_host.log(f'Added {events[i]} to the batch')
            i += 1
            continue

        if (event_data_batch._count == 0) :
            lambda_host.log('Message was too large and can not be sent until it is smaller')
            i += 1
            continue

        count = event_data_batch._count
        numEventsSent += count
        lambda_host.log(f'Batch is full - sending {count} messages in a single batch. Sent {numEventsSent} events so far')
        client.send_batch(event_data_batch)

        progressPercent = int(round(numEventsSent / len(events) * 100, -1))
        
        if progressPercent != progessSentToHost:
            progessSentToHost = progressPercent
            lambda_host.progress(progessSentToHost, 'Publishing events')

        can_add = True
        time.sleep(5)   # Without this sleep, the batch will be sent too fast and the event hub will reject the batch.
        event_data_batch = client.create_batch()

    count = event_data_batch._count
    if ( count > 0) :
        lambda_host.log(f'Sending remaining {count} messages as a single batch.')
        client.send_batch(event_data_batch)
        numEventsSent += count
    

    lambda_host.log(f'Sent {numEventsSent} events done.')

    if (numEventsSent != len(events)) :
      lambda_host.log(f'Not all messages were sent ({numEventsSent}/{len(events)})')

    client.close()
    lambda_host.log('Done submit_ts_events...')


def handle_dataframe(df_model:pd.DataFrame, timestamp:str, timestampId:str, spatialId: str, objectId: str, defaultObjectId:str, propertyIds:tuple, constant_spatial_id:str, constant_object_id:str):
    lambda_host.log(f'handle_dataframe:timestamp:{timestamp}|timestampId:{timestampId}|spatialId:{spatialId}|objectId:{objectId}|constant_spatial_id:{constant_spatial_id}|constant_object_id:{constant_object_id}')
    lambda_host.log(df_model.dtypes.to_string())
    lambda_host.log(df_model.head().to_string())
    if timestampId in df_model or timestamp is not None:
        eventsToSend = []
        for idx, row in df_model.iterrows():
            valid = False   
            spatial_value = '-'
            if spatialId and spatialId in row:
                spatial_value = row[spatialId]
                valid = True
            elif constant_spatial_id and constant_object_id:
                valid = True

            object_value = defaultObjectId
            if objectId and objectId in row:
                object_value = row[objectId]
                valid = True

            #lambda_host.log(f'valid:{valid}')
            if valid:
                #lambda_host.log(f'item:{object_value}')
                if timestampId:
                    try:
                        timestamp = str(row[timestampId])
                        if timestamp is 'None' or timestamp.strip() == '':
                            lambda_host.log(f'Mandatory timestamp value is empty for {row}. Please check the input file. Skipping this row.')
                            continue
                        if " " in timestamp:
                            if "AM" or "PM" in timestamp:
                                entry_date = time.mktime(datetime.datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S %p").timetuple())
                            else: 
                                entry_date = time.mktime(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").timetuple())
                        else:
                            entry_date = time.mktime(datetime.datetime.strptime(timestamp, "%Y-%m-%d").timetuple())
                        iso_time = datetime.datetime.fromtimestamp(entry_date).isoformat()
                    except:
                        lambda_host.log(f'Something went wrong converting the date for {timestamp}. Row:{row}. Please check the input file. Skipping this row.')
                        continue
                else:
                    iso_time = timestamp

                #lambda_host.log(f'iso_time:{iso_time}')
                eventObj = {
                    "time": iso_time,
                    "spatialId": constant_spatial_id if constant_spatial_id != '' else spatial_value, 
                    "objectId": constant_object_id if constant_object_id != '' else object_value,
                }
                validPropertyValueFound = False
                for propertyId in propertyIds:
                    if propertyId[0] in df_model:
                        validPropertyValueFound = True
                        eventObj[propertyId[1]] = float(row[propertyId[0]]) if is_number(row[propertyId[0]]) else (row[propertyId[0]] if not pd.isnull(row[propertyId[0]]) else '')

                if validPropertyValueFound:
                    eventsToSend.append(eventObj)
                    #if idx % 250 == 0:
                        #lambda_host.log(f'event to send JSON :{json.dumps(eventObj)}')
                        
        lambda_host.log(f'eventsToSend count:{len(eventsToSend)}')
        if len(eventsToSend) > 0:
            lambda_host.log(f'first event from the list to send to Time Series: {json.dumps(eventsToSend[0])}')
        submit_time_series_events(eventsToSend)    
    else:
        lambda_host.log(timestampId + ' column not found in dataframe or "timestamp" value was empty (' + timestamp + ').')

def publish_feed(entity_id:str, timestamp:str, timestamp_id:str, spatialId: str, objectId: str, defaultObjectId:str,  propertyIds:tuple, constant_spatial_id:str, constant_object_id:str):
    lambda_host.log(f'Publish feed calling timeseries')
    entity_path = lambda_host.download_entity_files(entity_id)
    if not os.path.isdir(entity_path):
        lambda_host.log('Error Raw product empty')
        exit_code(2)

    lambda_host.log(f'Raw Entity loaded successfully {entity_path}')
    
    types = ('*.ftr', 'report.csv')
    entity_files = []
    for files in types:
        entity_files.extend(glob.glob(entity_path + "\\" + files))

    lambda_host.log(f'entity_files:{entity_files}')

    for file_name in entity_files:
        entity_file = os.path.join(scrap_folder, file_name)
        lambda_host.log(f'feed file:{entity_file}')
        if entity_file:
            if file_name.endswith('.ftr'):
                df_model = pd.read_feather(entity_file)
            elif file_name.endswith('.csv'):
                df_model = pd.read_csv(entity_file)
            else:
                lambda_host.log(f'Unsupported file type {file_name}')
                exit_code(3)
            if not df_model.empty:
                handle_dataframe(df_model, timestamp, timestamp_id, spatialId, objectId, defaultObjectId, propertyIds, constant_spatial_id, constant_object_id)
            else:           
                lambda_host.log(f'file {file_name} is empty.')
                #exit_code(4)
    return {'success': True}

publish_feed(raw_entityId, timestamp, timestampId, spatialId, objectId, defaultObjectId, propertyIds, constant_spatial_id, constant_object_id)

lambda_host.set_exit_code(0)
lambda_host.log('Done publish reports...')