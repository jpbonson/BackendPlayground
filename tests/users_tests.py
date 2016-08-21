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
        config.configure_app(self.app, config_name = "testing")
        self.client = app.test_client()
        self.client.testing = True

        # initialize db
        open('tests/db_test.json', 'w').close()
        self.table = app.config['DATABASE'].table('users')
        user = {
            'id': 'maria',
        }
        self.table.insert(user)

    def tearDown(self):
        pass

    def test_db_initialized(self):
        query = Query()
        self.assertEqual(self.table.search(query.id == 'maria'), [{'id': 'maria'}])

    def test_users_status(self):
        result = self.client.get('/users')
        self.assertEqual(result.status_code, 200)

    def test_users_data(self):
        result = self.client.get('/users')
        self.assertEqual(json.loads(result.data), [{'id': 'maria'}])

    def test_get_user_that_exists_status(self):
        result = self.client.get('/users/maria')
        self.assertEqual(result.status_code, 200)

    def test_get_user_that_exists_data(self):
        result = self.client.get('/users/maria')
        self.assertEqual(json.loads(result.data), {'id': 'maria'})

    def test_get_user_that_doesnt_exist(self):
        result = self.client.get('/users/papainoel')
        self.assertEqual(result.status_code, 404)

    def test_create_new_user_status(self):
        result = self.client.post('/users', 
            data=json.dumps({'id': 'roberto'}), 
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 201)

    def test_create_new_user_data(self):
        user = {'id': 'roberto'}
        result = self.client.post('/users', 
            data=json.dumps(user), 
            headers={"content-type": "application/json"})
        self.assertEqual(json.loads(result.data), user)

    def test_create_new_user_db(self):
        result = self.client.post('/users', 
            data=json.dumps({'id': 'roberto'}), 
            headers={"content-type": "application/json"})
        self.assertEqual(self.table.search(Query().id == 'roberto'), [{'id': 'roberto'}])

    def test_try_create_user_that_already_exists(self):
        result = self.client.post('/users', 
            data=json.dumps({'id': 'maria'}), 
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 409)

    def test_try_create_invalid_user(self):
        result = self.client.post('/users', 
            data=json.dumps({'invalid_field': 'maria'}), 
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 400)

    def test_remove_user(self):
        result = self.client.delete('/user/maria')
        self.assertEqual(json.loads(result.data), [])

    def test_remove_user_db(self):
        result = self.client.delete('/user/maria')
        self.assertEqual(self.table.search(Query().id == 'maria'), [])

    def test_try_remove_user_that_doesnt_exist(self):
        result = self.client.delete('/user/papainoel')
        self.assertEqual(result.status_code, 404)

if __name__ == '__main__':
    unittest.main()