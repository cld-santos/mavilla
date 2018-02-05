from unittest import TestCase
from historian.tools.database import Database, Url


class TestDatabase(TestCase):

    def setUp(self):
        self.db = Database(db_name='ibm_test')

    def test_save_url(self):
        _url = self.db.save_url(Url(**{'url': 'http://claudio-santos.com'}))
        self.assertTrue(_url._id is not None)

    def test_url_uniqueness(self):
        self.db.save_url(Url(**{'url': 'http://claudio-santos.com'}))
        expected_exception = False
        try:
            self.db.save_url(Url(**{'url': 'http://claudio-santos.com'}))
        except:
            expected_exception = True

        self.assertTrue(expected_exception)

    def test_update_url(self):
        _url = self.db.save_url(Url(**{'url': 'http://claudio-santos.com'}))
        _url.processed = True
        res = self.db.update_url(_url)
        self.assertEqual(res, True)

    def test_update_url_with_kwargs(self):
        _url = self.db.save_url(Url(**{'url': 'http://claudio-santos.com'}))
        res = self.db.update_url(_url, processed=True)
        url_result = self.db.get_url_by(_url._id)
        self.assertEqual(url_result['processed'], True)
        self.assertEqual(res, True)


    def test_get_all_unprocessed(self):
        self.db.save_url(Url(**{'url': 'http://csantos.com'}))
        self.db.save_url(Url(**{'url': 'http://csantos.net'}))
        self.db.save_url(Url(**{'url': 'http://csantos.me'}))
        _url = self.db.save_url(Url(**{'url': 'http://claudio-santos.com'}))
        _url.processed = True
        self.db.update_url(_url)
        _url = self.db.save_url(Url(**{'url': 'http://simplologia.com.br'}))
        _url.processed = True
        self.db.update_url(_url)
        unprocessed = self.db.get_unprocessed_urls()
        processed = self.db.get_processed_urls()
        self.assertEqual(len(unprocessed), 3)
        self.assertEqual(len(processed), 2)

    def tearDown(self):
        self.db._client.drop_database('ibm_test')
