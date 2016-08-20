from app import app
import unittest 

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

if __name__ == '__main__':
    unittest.main()