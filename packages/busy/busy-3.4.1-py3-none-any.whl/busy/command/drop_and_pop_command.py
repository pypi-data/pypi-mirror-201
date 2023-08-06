# Drop moves item(s) to the bottom of a queue; Pop moves them to the top! These
# use default method (name of the command) and default method call (just pass in
# the criteria) so there's little code.

from ..command.command import QueueCommand


class DropCommand(QueueCommand):

    name = 'drop'
    key = 'r'
    prompt = "d(r)op"

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        self._add_criteria_arg(parser)

    @QueueCommand.wrap
    def execute(self):
        dropped = self.queue.drop(*self._criteria)
        if len(dropped) == 1:
            self.status = f"Dropped: {dropped[0].description}"
        elif dropped:
            self.status = f"Dropped {str(len(dropped))} Items"
        else:
            self.status = "Dropped nothing"


class PopCommand(QueueCommand):

    name = 'pop'
    key = 'o'
    prompt = "p(o)p"

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        self._add_criteria_arg(parser)

    @QueueCommand.wrap
    def execute(self):
        popped = self.queue.pop(*self._criteria)
        if len(popped) == 1:
            self.status = f"Popped: {popped[0].description}"
        elif popped:
            self.status = f"Popped {str(len(popped))} Items"
        else:
            self.status = "Popped nothing"
