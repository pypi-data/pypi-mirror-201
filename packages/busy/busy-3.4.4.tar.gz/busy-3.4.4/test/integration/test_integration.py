from unittest import TestCase
from tempfile import TemporaryDirectory

from busy.handler import main

class TestIntegration(TestCase):

    def test_add_task(self):
        with TemporaryDirectory() as t:
            c = f"--root {t} add --description t"
            main(*c.split())
            with open(f'{t}/tasks.txt') as f:
                l = f.readlines()[-1].strip()
                self.assertEqual(l, 't')