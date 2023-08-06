from unittest import TestCase
from unittest.mock import patch

from busy.util.python_version import confirm_python_version

class TestPythonVersion(TestCase):

    @patch('busy.util.python_version.version_info', (3, 0, 0, 'final', 0))
    def test_python_version_fail(self):
        self.assertRaises(RuntimeError, confirm_python_version, (3, 6, 5))

    @patch('busy.util.python_version.version_info', (3, 7, 0, 'final', 0))
    def test_python_version_pass(self):
        confirm_python_version, (3, 6, 5)
