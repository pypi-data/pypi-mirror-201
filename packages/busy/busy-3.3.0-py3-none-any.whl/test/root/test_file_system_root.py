from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from unittest.mock import MagicMock

from busy.queue.todo_queue import TodoQueue
from busy.root.file_system_root import FileSystemRoot
from busy.root.file_system_root import File
from busy.root.file_system_root import InvalidQueueNameError

class TestFileSystemRoot(TestCase):

    def test_root(self):
        with TemporaryDirectory() as d:
            sd = FileSystemRoot(Path(d))
            s = sd.get_queue('tasks')
            self.assertIsInstance(s, TodoQueue)

    def test_add_todo(self):
        with TemporaryDirectory() as td:
            sd1 = FileSystemRoot(Path(td))
            sd1.get_queue('x').add('a')
            sd1.save()
            sd2 = FileSystemRoot(Path(td))
            self.assertEqual(str(sd2.get_queue('x').top()), 'a')

    def test_make_dir_pater(self):
        with TemporaryDirectory() as td:
            r = FileSystemRoot(Path(td))
            r.get_queue('y').add('a')
            r.save()
            r2 = FileSystemRoot(Path(td))
            self.assertEqual(str(r2.get_queue('y').top()), 'a')

    def test_env_var_as_backup(self):
        with TemporaryDirectory() as td:
            with mock.patch.dict('os.environ', {'BUSY_ROOT': td}):
                sd1 = FileSystemRoot()
                sd1.get_queue('p').add('a')
                sd1.save()
                f = Path(td) / 'p.txt'
                self.assertEqual(f.read_text(), 'a\n')

    def test_user_root(self):
        with TemporaryDirectory() as td:
            with mock.patch.dict('os.environ', clear=True):
                with mock.patch('pathlib.Path.home', lambda: Path(td)):
                    sd1 = FileSystemRoot()
                    sd1.get_queue('w').add('a')
                    sd1.save()
                    f = Path(td) / '.busy' / 'w.txt'
                    self.assertEqual(f.read_text(), 'a\n')

    def test_list_queues(self):
        with TemporaryDirectory() as td:
            r = FileSystemRoot(Path(td))
            q1 = r.get_queue('a')
            q1.add('a')
            q2 = r.get_queue('b')
            q2.add('b')
            r.save()
            r2 = FileSystemRoot(Path(td))
            self.assertEqual(len(r2.queue_names), 2)

    def test_queue_not_start_with_dot(self):
        with TemporaryDirectory() as td:
            r = FileSystemRoot(Path(td))
            with self.assertRaises(InvalidQueueNameError):
                q = r.get_queue('.a')
        
