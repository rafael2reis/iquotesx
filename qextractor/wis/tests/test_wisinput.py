"""
Running the test: on the project root, type:

python -m unittest -v qextractor/wis/tests/test_wisinput.py
"""
import unittest

from qextractor.wis import wisinput
from qextractor.preprocessing import baseline
from qextractor.preprocessing import bosquequotes

class TestWisInput(unittest.TestCase):
    
    def setUp(self):
        self.corpus = bosquequotes.load()

    def tearDown(self):
        pass

    def testInterval(self):

        inte1 = wisinput.interval(self.corpus[3], 4)
        #print(inte1)

        resp1 = [(85, 102)]

        #[ print(k, v) for k, v in enumerate(qb) ]
        #[ print(e) for e in inte1 ]

        self.assertTrue(inte1 == resp1)

    def test_corefAnnotated(self):
        quotes = [[1,2],[6,8]]
        s = [['O', 'O'],\
            ['r1+', 'O'],\
            ['r1+', 'O'],
            ['O', 'O'],
            ['O', 'ref00'],
            ['O', 'O'],
            ['r1-', 'O'],
            ['r1-', 'O'],
            ['r1-', 'O']]
        gpqIndex = 0
        corefIndex = 1

        answer = [[4],[4]]

        coref, _ = wisinput.corefAnnotated(s, quotes, corefIndex, gpqIndex)

        self.assertEqual(coref, answer)

    def test_candidates(self):
        intervals, coref, corefLabels = wisinput.candidates(self.corpus[0])

        #print("intervals", intervals)
        #print("coref", coref)
        #print("corefLabels", corefLabels)

        self.assertTrue(len(intervals) == len(coref) == len(corefLabels) == 2)

    def test_scanCandidates(self):
        #print(self.corpus[0])
        candidates = wisinput.scanCandidates(self.corpus[0])

        #print('Length: ', len(candidates))
        #[ print(e) for e in candidates ]

        self.assertTrue(len(candidates) == 1)

if __name__ == '__main__':
    unittest.main()