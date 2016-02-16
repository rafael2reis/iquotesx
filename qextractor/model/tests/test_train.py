import unittest

from qextractor.model import train

class TestTrain(unittest.TestCase):

	def test_train(self):
		w = train.train()
		#print("w:", w)

		self.assertEqual(len(w), 537)

if __name__ == '__main__':
    unittest.main()