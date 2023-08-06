from .command import TodoCommand


# Returns the top task from the queue, without tags, a resource, or followons.

class BaseCommand(TodoCommand):

    name = "base"

    @TodoCommand.wrap
    def execute(self):
        return self.queue.base()
