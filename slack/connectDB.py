import pymongo
from logger import Logger
logger = Logger()


class MongoDBManager:
    def __init__(self):
        self.db_name = 'CRUD'
        self.client = None
        self.db = None
        self.collection = None


    def connect(self):
        self.client = pymongo.MongoClient()
        self.db = self.client[self.db_name]
        self.collection = self.db['users']
        logger.info("Connected to MongoDB")


    def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")


    def get_all_users(self):
        self.connect()
        user_list = []
        for user in self.collection.find():
            user['_id'] = str(user['_id'])
            user_list.append(user)
        self.disconnect()
        return user_list


    def get_user(self, id):
        self.connect()
        user = self.collection.find_one({'id':id})
        self.disconnect()
        return user


    def post_user(self, data):
        self.connect()
        user = self.collection.find_one({'id':data['id']})
        if user is None:
            result = self.collection.insert_one(data)
        else:
            result = None
        self.disconnect()
        return result


    def put_user(self, id, data):
        self.connect()
        user = self.collection.find_one({'id':id})
        if user is None:
            result = None
        else:
            result = self.collection.update_one({'id':id}, {'$set':data})
        self.disconnect()
        return result


    def del_user(self, id):
        self.connect()
        user = self.collection.find_one({'id':id})
        if user is None:
            result = None
        else:
            result = self.collection.delete_one({'id':id})
        self.disconnect()
        return result
                


connect = MongoDBManager()