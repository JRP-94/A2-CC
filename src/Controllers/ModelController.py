

import json
from typing import List
from urllib import response
from Models.user import User
from Models.login import Login
from Models.song import Song

class ModelController:
    
    def __init__(self, DBController) -> None:
        self.db = DBController
        self.Logins = list()
        self.users = list()
        
    def RegisterUser(self, username, email, password):
        self.Logins.append(Login(username, email, password))
        
    def GetLogins(self):
        response = self.db.GetAllLogins()
        for login in response['Items']:
            self.Logins.append(Login(login['username']['S'], login['email']['S'], login['password']['S']))
            print(login['username']['S'])
    
    def GetUser(self, email):
        subsName = self.db.GetSubs(email)
        
        subs = list()
        for song in subsName:
            temp = self.db.GetSong(song)
            subs.append(Song(temp['title'], temp['artist'], self.db.GetImage(temp['title']), temp['web_url'], temp['year']))
            
        username = ""
        for user in self.Logins:
            if(user.email == email):
                username = user.username
            
        user = User(email, username, subs)
        self.users.append(user)
        return user
    
    
    def AddSub(self, email, title):
        temp = self.db.GetSong(title) 
        for user in self.users:
            if user.email == email:
                user.subs.append(Song(temp['title'], temp['artist'], self.db.GetImage(temp['img_url']), temp['web_url'], temp['year']))
    
    def RemoveSub(self, email, title):
        for user in self.users:
            if user.email == email:
                for song in user.subs:
                    if song.title == title:
                        user.subs.remove(song)