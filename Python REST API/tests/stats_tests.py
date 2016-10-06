import unittest
import json
from app import app
from tinydb import Query
import config

class UserTests(unittest.TestCase): 

    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass 

    def setUp(self):
        # initialize app
        self.app = app
        config.configure_app(self.app, config_name = 'testing')
        self.client = app.test_client()
        self.client.testing = True

        # initialize db
        open('tests/db_test.json', 'w').close()

        self.table_users = app.config['DATABASE'].table('users')
        names = ['maria', 'joao', 'unpolular']
        for name in names:
            user = {
                'id': name,
            }
            self.table_users.insert(user)

        self.top10 = []
        self.maria_urls = []
        self.table_urls = app.config['DATABASE'].table('urls')

        url = {
            'id': '24096',
            'hits': 12,
            'url': 'bleh3',
            'userId': 'joao'
        }
        self.table_urls.insert(url)
        self.top10.append(url)

        url = {
            'id': '23095',
            'hits': 10,
            'url': 'blah2',
            'userId': 'maria'
        }
        self.table_urls.insert(url)
        self.top10.append(url)
        self.maria_urls.append(url)

        url = {
            'id': '24095',
            'hits': 6,
            'url': 'bleh2',
            'userId': 'joao'
        }
        self.table_urls.insert(url)
        self.top10.append(url)

        url = {
            'id': '23096',
            'hits': 5,
            'url': 'blah3',
            'userId': 'maria'
        }
        self.table_urls.insert(url)
        self.top10.append(url)
        self.maria_urls.append(url) 

        url = {
            'id': '23094',
            'hits': 1,
            'url': 'blah1',
            'userId': 'maria'
        }
        self.table_urls.insert(url)
        self.top10.append(url)
        self.maria_urls.append(url)

        for count in range(10):
            url = {
                'id': 'something',
                'hits': 0,
                'url': 'something_useless',
                'userId': 'unpopular'
            }
            self.table_urls.insert(url)
            if count < 5:
                self.top10.append(url)

        [x.pop('userId') for x in self.top10]
        [x.update({'shortUrl': 'http://localhost/'+x['id']}) for x in self.top10]
        [x.update({'shortUrl': 'http://localhost/'+x['id']}) for x in self.maria_urls]

    def tearDown(self):
        pass

    def test_get_url_stats_that_exists_status(self):
        result = self.client.get('/stats/23094')
        self.assertEqual(result.status_code, 200)

    def test_get_url_stats_that_exists_data(self):
        result = self.client.get('/stats/23094')
        url = {
            'id': '23094',
            'hits': 1,
            'url': 'blah1',
            'shortUrl': 'http://localhost/23094',
        }
        self.assertEqual(json.loads(result.data), url)

    def test_get_url_stats_that_doesnt_exist(self):
        result = self.client.get('/stats/42')
        self.assertEqual(result.status_code, 404)

    def test_get_url_stats_many_times_status(self):
        for _ in range(10):
            result = self.client.get('/stats/23094')
        self.assertEqual(result.status_code, 200)

    def test_get_global_stats_status(self):
        result = self.client.get('/stats')
        self.assertEqual(result.status_code, 200)

    def test_get_global_stats_correct_hits(self):
        result = self.client.get('/stats')
        self.assertEqual(json.loads(result.data)['hits'], 34)

    def test_get_global_stats_correct_urlcount(self):
        result = self.client.get('/stats')
        self.assertEqual(json.loads(result.data)['urlCount'], 15)

    def test_get_global_stats_correct_topurls(self):
        result = self.client.get('/stats')
        self.assertEqual(json.loads(result.data)['topUrls'], self.top10)

    def test_get_global_stats_for_empty_db(self):
        open('tests/db_test.json', 'w').close()
        result = self.client.get('/stats')
        expected = {
            'hits': 0,
            'urlCount': 0,
            'topUrls': [],
        }
        self.assertEqual(json.loads(result.data), expected)

    def test_get_global_stats_many_times_status(self):
        for _ in range(10):
            result = self.client.get('/stats')
        self.assertEqual(result.status_code, 200)

    def test_get_user_stats_status(self):
        result = self.client.get('/users/maria/stats')
        self.assertEqual(result.status_code, 200)

    def test_get_user_stats_that_doesnt_exist(self):
        result = self.client.get('/users/papainoel/stats')
        self.assertEqual(result.status_code, 404)

    def test_get_user_stats_correct_hits(self):
        result = self.client.get('/users/maria/stats')
        self.assertEqual(json.loads(result.data)['hits'], 16)

    def test_get_user_stats_correct_urlcount(self):
        result = self.client.get('/users/maria/stats')
        self.assertEqual(json.loads(result.data)['urlCount'], 3)

    def test_get_user_stats_correct_topurls(self):
        result = self.client.get('/users/maria/stats')
        self.assertEqual(json.loads(result.data)['topUrls'], self.maria_urls)

    def test_get_user_stats_many_times_status(self):
        for _ in range(10):
            result = self.client.get('/users/maria/stats')
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()