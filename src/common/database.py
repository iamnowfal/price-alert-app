import os

import pymongo

class Database(object):
    #URI = "mongodb://localhost:27017"
    #URI = "mongodb://<dbuser>:<dbpassword>@ds163698.mlab.com:63698/heroku_gxq89rk8"
    URI = os.environ.get("MONGOLAB_URI") # this will save the details in the heroku environment variables and thereby not visible for github users
    DATABASE = None


    @staticmethod
    def initialize(): #init(self) method is used ony in the context of creating objects with their own properties. for eg; different uri for dbs
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        db = Database.DATABASE[collection]
        db.insert(data)
        print "Successfully wrote data to %s database" % collection

        # here the db "posts" is considered as a collection(dictionary in fact) and data is inserted in it.

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True) ## this will try update. if not exists insert

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)

