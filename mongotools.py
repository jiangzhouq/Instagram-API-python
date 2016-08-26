#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo
from pymongo import MongoClient

class MongoTools:
    #client
    #db
    #usersCollection
    #mediasCollection

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.ins
        self.usersCollection = self.db.users
        self.mediasCollection = self.db.medias

    def insertUser(self, dict):
        if self.usersCollection.find({"username":dict["username"]}).count() > 0:
            result = False
            print(dict["username"], " already exists!")
        else:
            result = self.usersCollection.insert(dict)
            print(dict["username"], " added")
        return result

    def insertMedia(self, dict):
        result = self.mediasCollection.insert(dict)
        return result

    def getLastMediaTime(self,username):
        cursor = self.mediasCollection.find({"username": username})  
        print(cursor.count())  
        if cursor.count() == 0:
            return 0
        try:
            cursor.sort("created_time",-1)
            for i in cursor:
                print(i.get('created_time'))
                return(i.get('created_time'))
        except:
            return 0

    def getUsers(self):
        cursor = self.usersCollection.find()
        array = list(cursor)
        return array
