
from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date
import unittest

import busy.util.date_util

class TestDate(TestCase):

    @mock.patch('busy.util.date_util.today', lambda : Date(2019,2,11))
    def test_today(self):
        t = busy.util.date_util.relative_date('today')
        self.assertEqual(t, Date(2019, 2, 11))

