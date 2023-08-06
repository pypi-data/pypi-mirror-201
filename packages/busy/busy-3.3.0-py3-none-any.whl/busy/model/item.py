# A generic item from a queue, with a description and possibly tags

from csv import DictReader
from csv import DictWriter


class Item:

    schema = ['description']
    listfmt = "{1.description}"

    def __init__(self, description=None):
        assert isinstance(description, str)
        assert description
        self._description = description

    def __str__(self):
        return self._description

    @property
    def description(self):
        return self._description

    @classmethod
    def create(self, value):
        if isinstance(value, self):
            return value
        elif isinstance(value, str):
            return self(value)
        elif isinstance(value, dict):
            return self(**value)


    # A convenience method to get the tags from a string (description) as a set
    #
    # TODO: Do this with a regexp

    def _tags(self, string):
        words = string.split()
        return {w[1:].lower() for w in words if w.startswith('#')}


    # A convenience method to get the non-tags from a string (description) as a
    # string

    def _base(self, string):
        words = string.split()
        return ' '.join([w for w in words if not w.startswith('#')])


    # A property that is just the tags

    @property
    def tags(self):
        return self._tags(self.description)

    @property
    def base(self):
        return self._base(self.description)

# Read and write a set of items to or from a file-like object. This could be
# part of a root but could also be a tempfile.

def read_items(fileish, itemclass=Item):
    reader = DictReader(fileish, itemclass.schema, delimiter="|")
    return [itemclass.create(i) for i in reader if i]

def write_items(fileish, *items):
    schema = items[0].schema
    writer = DictWriter(fileish, schema, delimiter="|")
    for item in items:
        values = dict([(f, getattr(item, f)) for f in schema])
        writer.writerow(values)
