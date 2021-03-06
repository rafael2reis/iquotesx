import unittest

from pkg_resources import resource_filename
from qextractor.preprocessing import feature
from qextractor.preprocessing import globoquotes

GLOBOQUOTES_FILE = resource_filename('qextractor', 'data/corpus-globocom-cv.txt')

class TestFeature(unittest.TestCase):
    _corpus = None

    @classmethod
    def setUpClass(cls):
        cls._corpus = globoquotes.load(GLOBOQUOTES_FILE)
        
    def tearDown(self):
        pass

    def test_create(self):
        pass

    def test_pos(self):
        m = [[["NPROP"]], [["NPROP"]], [["PROADJ"]], [["N"]], [["PREP"]]]
        pos = feature.pos(m, 0)

        self.assertEqual(len(pos), 5)

    def test_binary(self):
        dic = {'corefPOSWin2=PREP': 0, 'corefPOSWin-4=None': 1, 'firstLetterUpperCaseNone': 2, 'distance6': 3}
        feat = [[['corefPOSWin2=PREP']], [['corefPOSWin-4=None','firstLetterUpperCaseNone']], \
            [['corefPOSWin2=PREP', 'corefPOSWin-4=None', 'firstLetterUpperCaseNone', 'distance6']]]
        result = [[[1,0,0,0,]], \
                    [[0,1,1,0]], \
                    [[1,1,1,1]]]

        bin = feature.binary(dic, feat)
        self.assertEqual(bin, result)

    def test_columns(self):
        pos = ["NPROP", "PROADJ", "N", "PREP"]

        c = feature.columns(pos)

        self.assertEqual(len(c), 108)

if __name__ == '__main__':
    unittest.main()