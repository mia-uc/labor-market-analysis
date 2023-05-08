from pymongo import MongoClient
import os

CONNECTED = """
#########################################################################
    Init Mongo Connection (ConnectionString = {connection_string}/{db}) 
#########################################################################
"""


class MongoInterfaces:
    def __init__(self, collection) -> None:
        connection_string = os.getenv("MONGO_CONN_STRING")
        db_name = os.getenv('MONGO_DB')
        client = MongoClient(connection_string)
        db = client[db_name]
        self.doc = db[collection]

        print(CONNECTED.format(connection_string=connection_string, db=db_name))

    def insert(self, entity):
        return self.doc.insert_one(entity)

    def exists(self, **question):
        return self.doc.find_one(question)

    def all(self, limit=0, skip=0, **condition):
        return self.doc.find(condition, limit=limit, skip=skip)

    def update(self, body, **keys):
        return self.doc.update_many(keys, {'$set': body})
