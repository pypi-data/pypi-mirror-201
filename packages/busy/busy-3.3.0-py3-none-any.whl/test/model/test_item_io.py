from unittest import TestCase
from unittest.mock import Mock
from tempfile import NamedTemporaryFile

from busy.model.item import Item
from busy.model.item import write_items
from busy.model.item import read_items

class TestItemIO(TestCase):

    def test_writer_tempfile(self):
        i = Mock()
        i.schema = ['d']
        i.d = 'a'
        with NamedTemporaryFile(mode="w+") as tempfile:
            write_items(tempfile, i)
            tempfile.seek(0)
            r = tempfile.readlines()
            self.assertEqual(r, ['a\n'])

    def test_reader_tempfile(self):
        ic = Mock()
        ic.schema = ['d']
        with NamedTemporaryFile(mode="w+") as tempfile:
            tempfile.writelines(['a\n'])
            tempfile.seek(0)
            ix = read_items(tempfile, ic)
            ic.create.assert_called_with({'d':'a'})
