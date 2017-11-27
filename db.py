import os
from pymongo import MongoClient

class bot_db(object):
    def __init__(self):
        self.db = self.MongoClient(os.environ["MONGO_DB_URI"]).slack_bot_db

    def write(self,data):
        self.db.hotels.insert_one(data)

    def read(self):
        response = []
        for obj in self.db.hotels.find():
            response.append(obj)
        return response

    def write_commands(self,keyword):
        try:
            itr = self.db.commands.find().next()
            itr["commands"].append(keyword)
            self.db.commands.save(itr)
        except StopIteration:
            itr = []
            itr.append(keyword)
            self.db.commands.insert_one({"commands":itr})

    def read_commands(self):
        response = []
        for res in self.db.commands.find():
            response = res["commands"]
        return response