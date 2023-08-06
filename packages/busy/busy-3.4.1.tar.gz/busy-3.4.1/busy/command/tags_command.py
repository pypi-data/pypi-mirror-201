from ..command.command import QueueCommand


class TagsCommand(QueueCommand):

    name = 'tags'

    @QueueCommand.wrap
    def execute(self):
        return '\n'.join(sorted(self.queue.tags()))
