import unittest
import json
from app import app
from tinydb import Query
from flask import url_for
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
        config.configure_app(self.app, config_name = "testing")
        self.client = app.test_client()
        self.client.testing = True

        # initialize db
        open('tests/db_test.json', 'w').close()

        self.table_users = app.config['DATABASE'].table('users')
        user = {
            'id': 'maria',
        }
        self.table_users.insert(user)

        self.table_urls = app.config['DATABASE'].table('urls')
        url = {
            "id": "23094",
            "hits": 0,
            "url": "https://github.com/jpbonson/TestingStuff",
            "shortUrl": "http://localhost:5000",
            "userId": "maria"
        }
        self.table_urls.insert(url)

    def tearDown(self):
        pass

    def test_redirect_v1_status(self):
        result = self.client.get('/urls/23094')
        self.assertEqual(result.status_code, 301)

    def test_redirect_v2_status(self):
        result = self.client.get('/23094')
        self.assertEqual(result.status_code, 301)

    def test_redirect_v1_for_invalid_url(self):
        result = self.client.get('/urls/nothing')
        self.assertEqual(result.status_code, 404)

    def test_redirect_v2_for_invalid_url(self):
        result = self.client.get('/nothing')
        self.assertEqual(result.status_code, 404)

    def test_redirect_v1_works(self):
        result = self.client.get('/urls/23094')
        self.assertEqual(result.location, "https://github.com/jpbonson/TestingStuff")

    def test_redirect_v2_works(self):
        result = self.client.get('/23094')
        self.assertEqual(result.location, "https://github.com/jpbonson/TestingStuff")

    def test_create_new_url_status(self):
        result = self.client.post('/users/maria/urls', 
            data=json.dumps({'url': 'https://www.google.com.br/'}), 
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 201)

    def test_create_new_url_data_correct_url(self):
        test_url = 'https://www.google.com.br/'
        result = self.client.post('/users/maria/urls', 
            data=json.dumps({'url': test_url}), 
            headers={"content-type": "application/json"})
        self.assertEqual(json.loads(result.data)['url'], test_url)

    def test_create_new_url_data_correct_hits(self):
        test_url = 'https://www.google.com.br/'
        result = self.client.post('/users/maria/urls', 
            data=json.dumps({'url': test_url}), 
            headers={"content-type": "application/json"})
        self.assertEqual(json.loads(result.data)['hits'], 0)

    def test_create_new_url_data_has_correct_keys(self):
        test_url = 'https://www.google.com.br/'
        result = self.client.post('/users/maria/urls', 
            data=json.dumps({'url': test_url}), 
            headers={"content-type": "application/json"})
        self.assertEqual(sorted(json.loads(result.data).keys()), ['hits', 'id', 'shortUrl', 'url'])

    def test_create_new_url_db(self):
        test_url = 'https://www.google.com.br/'
        result = self.client.post('/users/maria/urls', 
            data=json.dumps({'url': test_url}), 
            headers={"content-type": "application/json"})
        self.assertEqual(len(self.table_urls.search(Query().url == test_url)), 1)

    def test_try_create_url_for_invalid_user(self):
        result = self.client.post('/users/papainoel/urls', 
            data=json.dumps({'url': 'https://www.google.com.br/'}), 
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 404)

    def test_try_create_invalid_url(self):
        result = self.client.post('/users/maria/urls', 
            data=json.dumps({'not_url': 'https://www.google.com.br/'}), 
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 400)

    def test_remove_url(self):
        result = self.client.delete('/urls/23094')
        self.assertEqual(json.loads(result.data), [])

    def test_remove_url_db(self):
        result = self.client.delete('/urls/23094')
        self.assertEqual(self.table_urls.search(Query().id == '23094'), [])

    def test_try_remove_url_that_doesnt_exist(self):
        result = self.client.delete('/urls/42')
        self.assertEqual(result.status_code, 404)

if __name__ == '__main__':
    unittest.main()