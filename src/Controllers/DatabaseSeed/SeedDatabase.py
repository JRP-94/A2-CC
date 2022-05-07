from time import sleep
import boto3
import json

import requests

def SeedDatabase(tableName):
    dynamoClient = boto3.client('dynamodb')
    tables = dynamoClient.list_tables()['TableNames']
    
    if tableName not in tables:
        response = dynamoClient.create_table(
            AttributeDefinitions = [
                {
                    'AttributeName': 'title',
                    'AttributeType': 'S'
                }
            ],
            KeySchema = [
                {
                    'AttributeName': 'title',
                    'KeyType': 'HASH'
                }
            ],
            ProvisionedThroughput = {
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
            },
            TableName = tableName,
        )
        print(response['TableDescription']['TableStatus'])
        
        active = False
        while not active:
            response = dynamoClient.describe_table(TableName = tableName)
            if response['Table']['TableStatus'] == 'ACTIVE':
                active = True
                print(response['Table']['TableStatus'])
                print(active)
            else:
                sleep(1)
        
        if active:
            file = open('/home/jake/Desktop/dev/A2/src/Controllers/DatabaseSeed/a2.json')
            data = json.load(file)
        
            table = boto3.resource('dynamodb').Table(tableName)
            session = boto3.Session()
            s3 = boto3.resource('s3').Bucket('a2-images')
            
            
            for object in data['songs']:
                table.put_item(
                    TableName = tableName,
                    Item = object
                )
                # request = requests.get(object['img_url'], stream=True)
                # s3.upload_fileobj(request.raw, object['title'])
            
            file.close()
        
