from unittest import TestCase
from ..tools.database import Database, Url


class TestDatabase(TestCase):

    def setUp(self):
        self.db = Database(db_name='ibm_test')
        
    def test_save_url(self):
        _url = self.db.save_url(Url({'url': 'http://claudio-santos.com'}))
        self.assertTrue(_url._id is not None)

    def test_update_url(self):
        _url = self.db.save_url(Url({'url': 'http://claudio-santos.com'}))
        _url.processed = True
        res = self.db.update_url(_url)
        self.assertEqual(res, True)
        self.assertEqual(_url.processed, True)

    def test_get_all_unprocessed(self):
        self.db.save_url(Url({'url': 'http://csantos.com'}))
        self.db.save_url(Url({'url': 'http://csantos.net'}))
        self.db.save_url(Url({'url': 'http://csantos.me'}))
        _url = self.db.save_url(Url({'url': 'http://claudio-santos.com'}))
        _url.processed = True
        self.db.update_url(_url)
        _url = self.db.save_url(Url({'url': 'http://simplologia.com.br'}))
        _url.processed = True
        self.db.update_url(_url)
        unprocessed = self.db.get_unprocessed_urls()
        processed = self.db.get_processed_urls()
        self.assertEqual(len(unprocessed), 3)
        self.assertEqual(len(processed), 2)

    def tearDown(self):
        self.db._client.drop_database('ibm_test')
