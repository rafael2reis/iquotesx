import unittest

from qextractor.wis.wis import Task
from qextractor.wis import wis

class TestWis(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sortTasksByEnd(self):

        tasks = [Task(0,2,1,0), Task(1,4,1,0), Task(0,1,1,0)]
        tasksSorted = [Task(0,1,1,0), Task(0,2,1,0), Task(1,4,1,0)]

        tasks = wis.sortTasksByEnd(tasks)

        ends = [t.end for t in tasks]
        endsSorted = [t.end for t in tasksSorted]

        self.assertEqual(ends, endsSorted)

    def test_createPreviousArray(self):

        tasks = [Task(0,0,0,0), Task(0,1,1,0), Task(0,2,1,0), 
                        Task(1,4,1,0), Task(4,5,1,0), Task(2,6,1,0), Task(5,7,1,0)]

        p = wis.createPreviousArray(tasks)
        pCorrect = [0, 0, 0, 1, 3, 2, 4]

        self.assertEqual(p, pCorrect)

    def test_schedule(self):

        tasks = [Task(0,1,1,0), Task(0,2,1,0), 
                        Task(1,4,1,0), Task(4,5,1,0), Task(2,6,1,0), Task(5,7,1,0)]

        set_correct = [Task(0,1,1,0), Task(1,4,1,0), Task(4,5,1,0), Task(5,7,1,0)]
        max_w, set_tasks = wis.schedule(tasks)

        self.assertEqual(set_correct, set_tasks)

if __name__ == '__main__':
    unittest.main()