from unittest import TestCase

from busy.model.item import Item

class TestItem(TestCase):

    def test_tags(self):
        i = Item('a #b')
        tx = i.tags
        self.assertEqual(tx, {'b'})

    def test_tags_no_repeat(self):
        i = Item('a #b #b')
        tx = i.tags
        self.assertEqual(tx, {'b'})

    def test_base(self):
        i = Item('a b #c d e')
        w = i.base
        self.assertEqual(w, 'a b d e')
