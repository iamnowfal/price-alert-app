import uuid

from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query,
            "_id":self._id
        }
    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION, {"_id":self._id}, self.json())

    @classmethod
    def get_by_store_id(cls, store_id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"_id": store_id}))

    @classmethod
    def get_by_store_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"name":store_name}))

    # @classmethod
    # def get_from_database(cls,url_prefix):
    #     stores = [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {"url_prefix":{"$regex": '^{}'.format(url_prefix)}})]
    #     for store in stores:
    #         if store['tag_name'] == 'h1':
    #             return cls(**store)


    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix":{"$regex": '^{}'.format(url_prefix)}})) #input http://wwww.game to url_prefix and you get the store details

    @classmethod
    def find_by_url(cls, url):
        """
        return a store from a url like http://www.gamestop.com/item/Battelfield1/1123440
        :param url: the item's URL
        :return: a Store or StoreNotFoundException if no store matches URL.
        """
        for i in range(0, len(url)+1):
            try:
                store = cls.get_by_url_prefix(url[:i]) ##Query the database by each character of the url h, ht, http to find the match
                return store
            except:
                return StoreErrors.StoreNotFoundException("The URL couldn't match the available stores")
                ##return None ##you can also give 'pass' as return None is by default the response if not found anything

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]

    def delete_store(self):
        Database.remove(StoreConstants.COLLECTION, {"_id":self._id})