import unittest
import os
import sqlite3
import pipeline
class Test(unittest.TestCase):
    filePath = None
    @classmethod
    def setUpClass(cls):
        try:
            cls.filePath = pipeline.main()          
        except SystemExit:
            return           
        except Exception:
            raise
    def setUp(self):
        if(self.filePath is not None):
            self.conn = sqlite3.connect(self.filePath)
            self.cursor = self.conn.cursor()
        else:
            self.conn = self.cursor = None  
    def tearDown(self):
        if(self.conn is not None):
            self.conn.close()    
    def test_pipeline(self):
        self.assertIsNotNone(self.filePath, "Pipeline failed.")     
    def test_file(self):
        if(self.filePath is None):
            self.assertIsNotNone(self.filePath, "The file unavailable.")        
        else:
            self.assertTrue(os.path.exists(self.filePath), "The file unavailable.")

 
    @classmethod
    def tearDownClass(cls):       
        if hasattr(cls, 'cursor'):
            cls.cursor.close()
        if hasattr(cls, 'conn'):
            cls.conn.close()
        if cls.filePath:
            os.remove(cls.filePath) 


if __name__ == '__main__':
    unittest.main()