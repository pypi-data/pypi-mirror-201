from pathlib import Path
from tempfile import TemporaryDirectory
import os
import subprocess
from pathlib import Path

from platformdirs import user_data_dir

from busy.model.item import Item
from busy.queue.queue import Queue
from busy.model.item import read_items
from busy.model.item import write_items


class InvalidQueueNameError(Exception):
    pass


class File:


    # Takes a pathlib Path object to define the location

    def __init__(self, path):
        if path.stem.startswith('.'):
            raise InvalidQueueNameError
        self._path = path


    def read(self, itemclass=Item):
        if self._path.is_file():
            with open(self._path) as datafile:
                return read_items(datafile, itemclass)
        return []

    def save(self, *items):
        if items:
            with open(self._path, 'w') as datafile:
                write_items(datafile, *items)
        else:
            Path(self._path).write_text('')


class FileSystemRoot:

    def __init__(self, path=None):
        if not path:
            path = os.environ.get('BUSY_ROOT')
        if not path:
            path = user_data_dir(appname='Busy', appauthor = 'SteampunkWizard')
        self._path = Path(path) if not isinstance(path, Path) else path                
        if not self._path.is_dir():
            self._path.mkdir(parents=True)
        self._files = {}
        self._queues = {}

    @property
    def _str_path(self):
        return str(self._path.resolve())

    def get_queue(self, name):
        if name not in self._queues:
            queueclass = Queue.family_member('name', name) or Queue
            queuefile = File(self._path / f'{name}.txt')
            self._files[name] = queuefile
            items = queuefile.read(queueclass.itemclass)
            self._queues[name] = queueclass(self, items)
        return self._queues[name]

    def save(self):
        changed = False
        while self._queues:
            key, queue = self._queues.popitem()
            if queue.changed:
                items = queue.all()
                self._files[key].save(*items)
                changed = True

    @property
    def queue_names(self):
        filenames = list(self._path.glob('*.txt'))
        keys = [Path(f).stem for f in filenames]
        return keys
