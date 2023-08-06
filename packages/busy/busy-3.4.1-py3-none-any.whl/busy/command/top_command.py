# Get the top item from a Queue. Returns the entire description, including tags,
# resources, and followons.

from .command import QueueCommand


class TopCommand(QueueCommand):

    name = 'top'

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)

    @QueueCommand.wrap
    def execute(self):
        item = self.queue.top()
        if item is None:
            self.status = "No items in queue"
        else:
            return str(item)
