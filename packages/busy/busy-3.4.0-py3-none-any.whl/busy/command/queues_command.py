from ..command.command import Command


class QueuesCommand(Command):

    name = 'queues'

    @Command.wrap
    def execute(self):
        names = sorted(self._root.queue_names)
        return '\n'.join(names)
