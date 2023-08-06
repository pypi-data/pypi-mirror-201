from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch
from pathlib import Path

from busy.ui.ui import TerminalUI


class MockSubprocess:

    @staticmethod
    def run(arg):
        Path(arg[-1]).write_text('v')


class MockShUtil:

    @staticmethod
    def which(arg):
        return False


# Not really unit tests, relying on the UI class importing and using other
# stuff.

class TestEditor(TestCase):

    def test_edit_items(self):
        with patch('busy.ui.ui.subprocess', MockSubprocess):
            u = TerminalUI(None)
            ic = Mock()
            ic.schema = ['d']
            i = Mock()
            i.schema = ['d']
            i.d = 'a'
            new = u.edit_items(ic, i)
            ic.create.assert_called_with({'d':'v'})