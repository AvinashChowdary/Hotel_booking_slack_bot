import os
import json
from pymongo import MongoClient
from bson.json_util import dumps

class bot_db(object):
    def __init__(self):
        self.db = MongoClient(os.environ["MONGO_DB_URI"]).slack_bot_db

    def write(self,data):
        hotel = self.db.hotels
        id = hotel.insert_one(json.loads(str(data))).inserted_id
        return id

    def read(self):
        response = []
        for obj in self.db.hotels.find():
            response.append(obj)
        return response

    def get_booking(self, key):
        hotel = self.db.hotels
        booking = hotel.find({"booking_id": key })
        reply = dumps(booking)
        print(reply)
        return reply

    def delete_booking(self, id):
        hotel = self.db.hotels
        removed = hotel.remove({"booking_id" : id})
        print(removed)
        return 1