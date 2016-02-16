import unittest

from pkg_resources import resource_filename
from qextractor.preprocessing import globoquotes

GLOBOQUOTES_FILE = resource_filename('qextractor', 'data/corpus-globocom-cv.txt')

class TestGloboQuotes(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load(self):
        print("test_load")

        corpus = globoquotes.load(GLOBOQUOTES_FILE)

        #print("len corpus: ", len(corpus))
        #print("len 0: ", len(corpus[0]))
        #print("corpus[0]", len(corpus[0]), " corpus[0][0]=", len(corpus[0][0]))

        #[print(x) for x in corpus[0]]

        self.assertTrue(len(corpus) == 551 and len(corpus[0]) == 774)

if __name__ == '__main__':
    unittest.main()