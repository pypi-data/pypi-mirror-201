from ..command.command import TodoCommand


# Get the resource (a URL) for the top entry in a queue

class ResourceCommand(TodoCommand):

    name = "resource"

    @TodoCommand.wrap
    def execute(self):
        return str(self.queue.resource() or '')
