from .queue import Queue
from ..model.task import Task
from ..model.task import Plan
from ..model.task import DoneTask


# TODO: Move type-specific methods to specific commands

class TodoQueue(Queue):

    itemclass = Task
    name = 'tasks'

    def __init__(self, root=None, items=[]):
        super().__init__(root, items)
        self._plans = None
        self._done = None

    @property
    def plans(self):
        if not self._plans:
            if self.root:
                self._plans = self.root.get_queue(PlanQueue.name)
            else:
                self._plans = PlanQueue()
        return self._plans

    @property
    def done(self):
        if not self._done:
            if self.root:
                self._done = self.root.get_queue(DoneQueue.name)
            else:
                self._done = DoneQueue()
        return self._done


    def defer(self, *indices, date):
        plans = [self.top(i).as_plan(date) for i in indices]
        self.plans.add(*plans)
        self.delete(*indices)
        return plans


    # The indices passed to the activate method are on the plans queue, not this
    # queue.

    def activate(self, *indices):
        tasks = [self.plans.top(i).as_todo() for i in indices]
        added = self.add(*tasks, index=0)
        self.plans.delete(*indices)
        return added


    def finish(self, *indices, date):
        donelist, keeplist = self._split_by_indices(*indices)
        self._items = keeplist
        finished = [t.as_done(date) for t in donelist]
        self.done.add(*finished)
        added = [t for t in [tt.as_followon() for tt in donelist] if t]
        self.add(*added)
        deferred = [t for t in [tt.as_repeat() for tt in donelist] if t]
        self.plans.add(*deferred)
        return (finished, added, deferred)

    def resource(self, index=1):
        return self._items[index-1].resource if self._items else None

    def base(self, index=1):
        return self._items[index-1].base if self._items else None


class PlanQueue(Queue):
    itemclass = Plan
    name = 'plans'


class DoneQueue(Queue):
    itemclass = DoneTask
    name = 'done'
