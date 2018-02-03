from pymongo import MongoClient
from bson.objectid import ObjectId 


class Url():
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.processed = kwargs.get('processed', False)
        self.parent = kwargs.get('parent', None)
        self._id = kwargs.get('_id', None)

    def to_dict(self):
        _url = self.__dict__
        _url['_id'] = str(_url['_id'])
        return _url


class Database():
    def __init__(self, db_name='ibm'):
        self._client = MongoClient('mongodb://localhost:27017/')
        self._database = self._client[db_name]
        self.db = self._database.investigation
        self.db.create_index('url', unique=True)

    def save_url(self, url):
        _url_dict = url.__dict__
        del _url_dict['_id']
        insert_result = self.db.insert_one(_url_dict)
        url._id = insert_result.inserted_id
        return url

    def update_url(self, url):
        if not isinstance(url._id, ObjectId):
            url._id = ObjectId(url._id)
        try:
            self.db.update_one(
                { '_id':  url._id},
                { '$set': url.__dict__ }
            )
            return True
        except Exception as e:
            print(e)
            return False

    def get_unprocessed_urls(self):
        res = []
        for item in self.db.find({'processed': False}):
            item['_id'] = str(item['_id'])
            res.append(item)

        return res

    def get_processed_urls(self):
        res = [Url(**item) for item in self.db.find({'processed': True})]
        return res

    def get_all_urls(self):
        res = [Url(**item) for item in self.db.find()]
        return res
