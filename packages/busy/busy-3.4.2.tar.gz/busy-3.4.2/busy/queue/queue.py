# General-purpose queue of items. Method calls on queue use indices that start
# at 1. A queue doesn't know it's own name.
#
# TODO: Make Queue not a ClassFamily
# TODO: Queue belongs under model

import random
from pathlib import Path

from busy.selector import Selector
from busy.model.item import Item
from busy.util.class_family import ClassFamily


# TODO: Use a Python builtin to make Queue list-like.

class Queue(ClassFamily):

    itemclass = Item

    def __init__(self, root=None, items=[]):
        self.root = root
        self.changed = False
        self._items = [self.itemclass.create(i) for i in items if i]


    # Take "criteria" (such as tags, ranges of numbers, etc) and return the
    # indices of the resulting items. In other parts of the class and
    # subclasses, operations need to know what items to act on.
    #
    # Both "criteria" and "indices" start with 1, so have to be adjusted
    # internally here when handling the _items list.
    
    def indices(self, *criteria):
        selector = Selector(criteria)
        return [i+1 for i in selector.indices(self._items)]

    def items(self, *indices):
        return [self._items[i-1] for i in indices]


    # Every item has a string representation; this method returns it
    # TODO: I removed the default to all. Is that OK?

    def strings(self, *indices):
        return [str(self._items[i-1]) for i in indices]

    # Return a list of tuples (index, item) based on criteria. Remember that
    # criteria start with an index of 1, but indices start at zero.
    # TODO: Eliminate this one

    def list(self, *criteria):
        return [(i, self._items[i-1]) for i in self.indices(*criteria)]


    def all(self):
        return self._items

    def count(self):
        return len(self._items)


    # Add new items. Always makes them the right class. Also does inserts.

    def add(self, *items, index=None):
        newitems = [self.itemclass.create(i) for i in items if i]
        index = len(self._items) if index is None else index
        self._items[index:index] = newitems
        self.changed = True
        return newitems


    # Replace existing items at the indices provided. Also inserts if the
    # indices run out. Does not create items; expects them to already exist.
    # Indices start at 1, so have to be adjusted going into the _items list.
    # Unlike other methods, it takes raw lists, not unpacked. Does not return
    # anything since the calling code already has the new items. Because the
    # list pop operations are destructive, act on copies of the lists, so the
    # calling code can still use them afterwards.
    
    def replace(self, indices, newvalues):
        _indices = indices.copy()
        _newvalues = newvalues.copy()
        while _newvalues and _indices:
            self._items[_indices.pop(0)-1] = _newvalues.pop(0)
        while _indices:
            del self._items[_indices.pop()-1]
        self._items.extend(_newvalues)
        self.changed = True


    # Used to be called "get" and maybe that was better. Retrieve one item. Used
    # by the "top" command, which is set to always retrieve the first item.

    def top(self, index=1):
        return self._items[index-1] if self._items else None


    def _split(self, *criteria):
        return self._split_by_indices(*self.indices(*criteria))

    def _split_by_indices(self, *indices):
        inlist = [t for i, t in enumerate(self._items) if i+1 in indices]
        outlist = [t for i, t in enumerate(self._items) if i+1 not in indices]
        return (inlist, outlist)


    def pop(self, *criteria):
        if not criteria:
            criteria = [len(self._items)]
        hilist, lolist = self._split(*criteria)
        self._items = hilist + lolist
        self.changed = (len(hilist) > 0)
        return hilist

    def drop(self, *criteria):
        if not criteria:
            criteria = [1]
        lolist, hilist = self._split(*criteria or [1])
        self._items = hilist + lolist
        self.changed = True
        return lolist

    def delete(self, *indices):
        killlist, keeplist = self._split_by_indices(*indices)
        self._items = keeplist
        self.changed = True
        return killlist


    # TODO: Remove the manage operation. Just use list and replace.

    # def manage(self, *criteria, editor):
    #     itemlist = self.list(*criteria)
    #     indices = [i[0]-1 for i in itemlist]
    #     items = [i[1] for i in itemlist]
    #     new_items = editor(self.itemclass, *items)  # move this out to the command and/or UI level
    #     self.replace(indices, new_items)


    # TODO: Bring back the shuffle command

    def shuffle(self, *criteria):
        itemlist = self.list(*criteria)
        indices = [i[0]-1 for i in itemlist]
        items = [i[1] for i in itemlist]
        random.shuffle(items)
        self.replace(indices, items)


    # Get all the tags for the queue. Neat Python trick: return a Set!

    def tags(self):
        master = [i.tags for i in self._items]
        return {item for sublist in master for item in sublist}
