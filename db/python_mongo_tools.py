from pymongo import MongoClient
import os
import logging
from datetime import datetime

log = logging.getLogger(__name__)
CONNECTED = """Init Mongo Connection (ConnectionString = {connection_string}/{db}"""


class MongoInterfaces:
    def __init__(self, collection) -> None:
        connection_string = os.getenv("MONGO_CONN_STRING")
        db_name = os.getenv('MONGO_DB')
        client = MongoClient(connection_string)
        db = client[db_name]
        self.doc = db[collection]

        log.info(CONNECTED.format(
            connection_string=connection_string,
            db=db_name
        ))

    def insert(self, entity: dict):
        entity['created_at'] = datetime.utcnow()
        return self.doc.insert_one(entity)

    def exists(self, **question):
        return self.doc.find_one(question)

    def all(self, limit=0, skip=0, sort=None, **condition):
        return self.doc.find(condition, limit=limit, skip=skip, sort=sort).max_time_ms(10 * 60 * 1000)

    def update(self, body, **keys):
        return self.doc.update_many(keys, {'$set': body})
