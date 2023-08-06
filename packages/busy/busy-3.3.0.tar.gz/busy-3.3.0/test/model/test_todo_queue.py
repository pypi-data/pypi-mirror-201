from unittest import TestCase
import datetime

from busy.model.task import Task
from busy.queue.todo_queue import TodoQueue
from busy.model.task import Plan

# TODO: Clean this up so it doesn't require Task
# TODO: Clean this up so it doesn't depend on defer for other methods

class TestTodoQueue(TestCase):

    def test_top(self):
        q = TodoQueue()
        q.add(Task('a'))
        t = q.top()
        self.assertEqual(str(t),'a')

    def test_list(self):
        s = TodoQueue()
        s.add(Task('a'))
        s.add(Task('b'))
        i = s.list()
        self.assertEqual(len(i), 2)
        self.assertEqual(i[1][0], 2)
        self.assertEqual(str(i[0][1]), 'a')
        self.assertIsInstance(i[1][1], Task)

    def test_defer(self):
        s = TodoQueue()
        s.add(Task('a'))
        d = datetime.date(2018,12,25)
        s.defer(*[1], date=d)
        self.assertEqual(s.plans.count(), 1)
        self.assertEqual(s.plans.top(1).date.year, 2018)

    def test_pop(self):
        s = TodoQueue()
        t1 = Task('a')
        t2 = Task('b')
        s.add(t1)
        s.add(t2)
        s.pop()
        i = s.list()
        self.assertEqual(len(i), 2)
        self.assertEqual(str(i[0][1]), 'b')

    def test_by_number(self):
        s = TodoQueue()
        s.add(Task('a'))
        s.add(Task('b'))
        t = s.top(2)
        self.assertEqual(str(t), 'b')

    def test_create_with_string(self):
        s = TodoQueue()
        s.add('a')
        self.assertEqual(str(s.top()), 'a')
        self.assertIsInstance(s.top(), Task)

    def test_create_with_multiple_strings(self):
        s = TodoQueue()
        s.add('a','b','c')
        self.assertIsInstance(s.top(), Task)
        self.assertEqual(s.count(), 3)
        self.assertEqual(str(s.top(2)), 'b')

    def test_select_multiple(self):
        s = TodoQueue()
        s.add('a','b','c')
        t = s.indices(1,3)
        self.assertEqual(len(t), 2)

    def test_list_plans(self):
        s = TodoQueue()
        s.add('a','b')
        s.defer(0, date=(2018,12,4))
        self.assertEqual(s.plans.count(), 1)

    def test_defer_by_index(self):
        s = TodoQueue()
        s.add('a','b')
        s.defer(1, date=(2018,12,4))
        t = s.top()
        self.assertEqual(s.plans.count(),1)
        self.assertEqual(str(t), 'b')

    def test_defer_multiple(self):
        s = TodoQueue()
        s.add('a','b','c')
        s.defer(1, 3, date=(2018,12,5))
        p = s.plans.top(2)
        self.assertEqual(str(p), 'c')

    def test_list_by_criteria(self):
        s = TodoQueue()
        s.add('a','b','c')
        i = s.list(2,3)
        self.assertEqual(len(i), 2)
        self.assertEqual(str(i[1][1]), 'c')

    def test_drop(self):
        s = TodoQueue()
        s.add('a','b','c')
        s.drop()
        self.assertEqual(str(s.top()), 'b')
        self.assertEqual(str(s.top(3)), 'a')

    def test_drop_by_criteria(self):
        s = TodoQueue()
        s.add('a','b','c','d')
        s.drop('2-3')
        self.assertEqual(str(s.top(1)), 'a')
        self.assertEqual(str(s.top(2)), 'd')
        self.assertEqual(str(s.top(3)), 'b')
        self.assertEqual(str(s.top(4)), 'c')

    def test_activate(self):
        s = TodoQueue()
        s.add('a','b')
        s.defer(1, 2, date=(2018,12,4))
        s.activate(2)
        t = s.top()
        self.assertEqual(str(t), 'b')

    def test_done_no_manager(self):
        s = TodoQueue()
        d = s.done
        self.assertIsNotNone(d)


    # Eliminate blank followons

    def test_finish_output(self):
        s = TodoQueue()
        s.add('a','b')
        f, a, d = s.finish(0, 1, date=(2023,2,12))
        self.assertEqual(a, [])
        self.assertEqual(d, [])


    def test_base(self):
        q = TodoQueue()
        q.add('a at xy #b #c --> repeat tomorrow')
        b = q.base()
        self.assertEqual(b, 'a')

    def test_plans_indices(self):
        q = TodoQueue()
        p = Plan('g',(2023,4,5))
        q.plans.add(p)
        ix = q.plans.indices(1)
        self.assertEqual(ix, [1])