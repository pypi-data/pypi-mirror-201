from pathlib import Path
from tempfile import TemporaryDirectory
import os
import subprocess
from pathlib import Path

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
        if path:
            self._path = Path(path) if isinstance(path, str) else path
            assert isinstance(self._path, Path) and self._path.is_dir()
        else:
            env_var = os.environ.get('BUSY_ROOT')
            self._path = Path(env_var if env_var else Path.home() / '.busy')
            if not self._path.is_dir():
                self._path.mkdir()
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
