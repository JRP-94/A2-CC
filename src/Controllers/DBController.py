from email.headerregistry import ContentTypeHeader
import boto3
from boto3.dynamodb.conditions import Key, And
from functools import reduce



class DBController:

    def __init__(self) -> None:
        self.dynamoClient = boto3.client('dynamodb')
        self.loginTable = boto3.resource('dynamodb').Table("login")
        self.userTable = boto3.resource('dynamodb').Table("user")
        self.musicTable = boto3.resource('dynamodb').Table("music")
        session = boto3.Session()
        self.s3 = boto3.client('s3')

    def GetAllLogins(self):
        return self.dynamoClient.scan(TableName='login')
    
    def Register(self, username, email, password):
        self.loginTable.put_item(
            TableName = 'login',
            Item = {
                "username": username,
                "email": email,
                "password": password 
            }
        )
    
    def SearchMusic(self, filters):
        response = self.musicTable.scan(FilterExpression=reduce(And, ([Key(key).eq(value) for key, value in filters.items()])))['Items']
        print(response)
        return response
        
    def GetSong(self, title):
        return self.musicTable.get_item(Key={'title': title})['Item']
    
    def GetImage(self, title):
        
        url = self.s3.generate_presigned_url(
            "get_object",
            ExpiresIn=30,
            Params={
                "Bucket": 'a2-images',
                "Key": title,
                }
        )
        print(url)
        return url
        
    def RemoveSub(self, email, title):
        response = self.userTable.delete_item(
            Key={
                'email': email,
                'song': title
            }
        )
        print(response)
    
    def AddSub(self, email, title):
        response = self.userTable.put_item(
            Item={
                'email': email,
                'song': title
            }
        )
        print(response)
    
    def GetSubs(self, email):
        filter = Key('email').eq(email)
        response = self.userTable.query(
            KeyConditionExpression = filter
            )
        subs = []
        for item in response['Items']:
            subs.append(item['song'])
        return subs