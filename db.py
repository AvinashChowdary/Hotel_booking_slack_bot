import os
from pymongo import MongoClient

class bot_db(object):
    def __init__(self):
        self.mongodb = MongoClient(os.environ["MONGO_DB_URI"])
        self.db = self.client.slack_bot_db

    def write(self,data):
        self.db.hotels.insert_one(data)

    def read(self):
        response = []
        for obj in self.db.hotels.find():
            response.append(obj)
        return response