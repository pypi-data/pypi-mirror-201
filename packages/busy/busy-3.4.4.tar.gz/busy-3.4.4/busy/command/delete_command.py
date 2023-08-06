from ..command.command import QueueCommand


class DeleteCommand(QueueCommand):

    name = 'delete'
    key = 'd'
    prompt = 'd)elete'

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        parser.add_argument('--yes', action='store_true')
        self._add_criteria_arg(parser)


    # TODO: Make a convenience method to set the default

    def clean_args(self):
        super().clean_args()
        if self.is_omitted('criteria'):
            self._namespace.criteria = [1]
        if self._indices:
            self._ui.output('\n'.join(self._strings))
            self.confirm(f"Delete {self.count()}")

    # Assume the indices have been already set, before confirmation.

    @QueueCommand.wrap
    def execute(self):
        if self._namespace.yes:
            deleted = self.queue.delete(*self._indices)
            self.status = f"Deleted {self.count(deleted)}"
        else:
            self.status = "Delete command canceled"
