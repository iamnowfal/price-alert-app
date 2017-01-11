import uuid


import requests
import bs4 as bs
import src.models.items.constants as ItemConstants
from src.common.database import Database
from src.models.stores.store import Store


class Item(object):
    def __init__(self,url, name,  price=None, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        ##store = Store.get_from_database(url)
        self.tag_name = store.tag_name
        self.query = store.query
        ##self.price = self.load_price() if price is None else price ##if user has ten items on alerts page, give each search for price takes 5 secs, it is going to take 50 seconds to load the page
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex  if _id is None else _id



    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_name(self, tag_name,query):
        pass

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id":item_id}))


    def load_price(self): ## we can extend this program by adding one more query,tagname to find the item name.
        #request = requests.get('http://www.gamestop.com/ps4/games/battlefield-1/129210')
        request = requests.get(self.url)
        content = request.content
        soup=bs.BeautifulSoup(content, 'html.parser')
        #print soup.prettify()
        bf1_element = soup.find_all(self.tag_name,self.query)
        for item in bf1_element:
            bf1_price = float(item.find('span').text)
            self.price = bf1_price
            print self.price
        # bf1_tag = soup.find_all('div', {"class":"buy1 ats-prodBuy-buyBoxSec"})
        # for item in bf1_tag:
        #     bf1_price = item.find_all('span')

    def save_to_db(self):
        #Database.insert(ItemConstants.COLLECTION, data=self.json())
        Database.update(ItemConstants.COLLECTION, {"_id":self._id}, self.json())

    @classmethod
    def get_by_item_id(cls,item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id":item_id}))

    def json(self):
        return {
            "name": self.name,
            "url": self.url,
            "_id": self._id,
            # "store": self.store,
            "price": self.price
        }