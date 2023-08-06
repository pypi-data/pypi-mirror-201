from curses import echo, noecho, newwin
from ..command.command import QueueCommand


class AddCommand(QueueCommand):

    name = 'add'
    key = 'a'

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        parser.add_argument('--description', nargs='?')

    def clean_args(self):
        super().clean_args()
        if self.is_omitted('description'):
            description = self._ui.get_string("Description")
            self._namespace.description = description
    

    # TODO: Support multiple adds at once    

    @QueueCommand.wrap
    def execute(self):
        description = self._namespace.description
        if description:
            self.queue.add(description)
            self.status = "Added: " + description
        else:
            self.status = "Nothing added"
