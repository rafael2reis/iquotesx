import unittest

from pkg_resources import resource_filename
from qextractor.preprocessing import preprocessing

INPUT_FILE = resource_filename('qextractor', 'data/gen/qextractor_input_test.csv')

class TestPreprocessing(unittest.TestCase):
        
    def tearDown(self):
        pass

    def test_createInput(self):
    	preprocessing.createInput()

    	self.assertTrue(True)

    def test_createInputTest(self):
    	preprocessing.createInput(fileName=INPUT_FILE, createTest=True)

    	self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()