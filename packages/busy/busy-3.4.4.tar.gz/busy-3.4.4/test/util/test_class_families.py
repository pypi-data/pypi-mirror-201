from unittest import TestCase

from busy.ui.ui import UI
from busy.queue.queue import Queue
from busy.handler import Handler
from busy.command.command import Command
from busy.command.finish_command import FinishCommand


class TestClassFamilies(TestCase):

    def test_import_ui(self):
        ui_classes = UI.__subclasses__()
        self.assertEqual(len(ui_classes), 1)

    def test_import_queue(self):
        queue_classes = Queue.family_members()
        self.assertEqual(len(queue_classes), 4)

    def test_import_command(self):
        classes = Command.family_members('name')
        self.assertTrue(FinishCommand in classes)
    
    def test_specific_command(self):
        finish_class = Command.family_member('name', 'finish')
        self.assertEqual(finish_class, FinishCommand)
