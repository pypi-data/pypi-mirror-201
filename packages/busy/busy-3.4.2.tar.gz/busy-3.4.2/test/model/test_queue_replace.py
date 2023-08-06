from unittest import TestCase

from busy.queue.queue import Queue

class TestQueueReplace(TestCase):

    def test_replace_one(self):
        a = Queue()
        a.add('a','b','c')
        a.replace([2], ['d'])
        self.assertEqual(str(a.top(2)), 'd')

    def test_replace_multi(self):
        a = Queue()
        a.add('a','b','c','d')
        a.replace([2,3], ['1','2'])
        self.assertEqual(a.strings(1,2,3,4), ['a','1','2','d'])

    def test_replace_extra_index(self):
        a = Queue()
        a.add('a','b','c','d')
        a.replace([2,3], ['1'])
        self.assertEqual(a.strings(1,2,3), ['a','1','d'])
