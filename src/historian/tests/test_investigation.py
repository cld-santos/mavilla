from unittest import TestCase
from historian.tools.database import Database, Url
from historian.tools.investigation import Investigation


class TestInvestigation(TestCase):

    def setUp(self):
        self.db = Database(db_name='ibm_test')
        self.investigation = Investigation(database=self.db)

    def test_register_unprocessed(self):
        unprocessed_urls = ['http://csantos.net', 'http://csantos.com', 'http://csantos.me']
        self.db.save_url(Url(**{'url': 'http://csantos.com', 'processed': True}))
        self.investigation.register_unprocessed_urls(unprocessed_urls)
        unprocessed = self.db.get_unprocessed_urls()
        processed = self.db.get_processed_urls()
        self.assertEqual(len(unprocessed), 2)
        self.assertEqual(len(processed), 1)

    def tearDown(self):
        self.db._client.drop_database('ibm_test')
