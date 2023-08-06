from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

from busy.handler import Handler

class TestHandler(TestCase):

    def test_init_passing_args_to_command(self):
        r = Mock()
        n = Mock()
        n.root = "r"
        n.command = "c"
        with patch('busy.handler.FileSystemRoot', lambda m: r):
            with patch('busy.handler.Command') as C:
                cc = Mock()
                cc.ui = None
                C.family_member = lambda a, b: cc
                with patch('busy.handler.UI') as U:
                    h = Handler(n)
                    cc.assert_called_with(root=r, ui=h.ui, namespace=n)

    @patch('busy.handler.FileSystemRoot', Mock())
    def test_get_command(self):
        n = Mock()
        n.command = 'c'
        u = Mock()
        with patch('busy.handler.Command') as C:
            with patch('busy.handler.UI') as U:
                cc = Mock()
                cc.ui = None
                C.family_member = lambda a, b: cc
                h = Handler(n)
                C.family_member = Mock()
                c = h.get_command('k', 'a', ui=u)
                C.family_member.assert_called_with('k','a')

