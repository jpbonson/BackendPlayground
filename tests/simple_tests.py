import unittest
from app import app
from tinydb import TinyDB, Query

class SimpleTests(unittest.TestCase): 

    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass 

    def test_home_status_code(self):
        result = self.app.get('/') # sends HTTP GET request
        self.assertEqual(result.status_code, 200)

    def test_home_data(self):
        result = self.app.get('/') # sends HTTP GET request
        self.assertEqual(result.data, "Hello World!")

    def test_working_db(self):
        db_path = 'tests/db_test.json'
        open(db_path, 'w').close()
        db = TinyDB(db_path)
        User = Query()
        db.insert({'name': 'John', 'age': 22})
        self.assertEqual(db.search(User.name == 'John'), [{u'age': 22, u'name': u'John'}])

if __name__ == '__main__':
    unittest.main()