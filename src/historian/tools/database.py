import json
from pymongo import MongoClient
from bson.objectid import ObjectId 
from historian.celery import app


class Url():
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.processed = kwargs.get('processed', False)
        self.parent = kwargs.get('parent', None)
        self.child_task_id = kwargs.get('child_task_id', None)
        self._id = kwargs.get('_id', None)

    def to_dict(self):
        _url = self.__dict__
        _url['_id'] = str(_url['_id'])
        return _url

    def __repr__(self):
        return json.dumps(self.to_dict())


class Database():
    def __init__(self, db_name='ibm', collection=None):
        self._client = MongoClient('mongodb://localhost:27017/')
        self._database = self._client[db_name]
        self.db = self._database[collection if collection else 'investigation']
        self.db.create_index('url', unique=True)

    def save_url(self, url):
        _url_dict = url.__dict__
        del _url_dict['_id']
        insert_result = self.db.insert_one(_url_dict)
        url._id = insert_result.inserted_id
        return url

    def update_url(self, url, **kwargs):
        if not isinstance(url._id, ObjectId):
            url._id = ObjectId(url._id)
        try:
            self.db.update_one(
                { '_id':  url._id},
                { '$set': url.__dict__ if len(kwargs) == 0 else kwargs}
            )
            return True
        except Exception as e:
            print(e)
            return False

    def get_url_by(self, _id):
        if not isinstance(_id, ObjectId):
            _id = ObjectId(_id)

        return self.db.find_one({'_id': _id})

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

    def kill_them_all(self, collection):
        cursor = self._database[collection].find()
        for item in cursor:
            result = app.AsyncResult(item['child_task_id'])
            result.revoke(terminate=True)
