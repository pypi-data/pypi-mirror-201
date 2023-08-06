
from .command import QueueCommand
import busy


class EditorCommandBase(QueueCommand):

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        self._add_criteria_arg(parser)


    # Relies on subclasses setting the _default_criterium attribute.

    def clean_args(self):
        super().clean_args()
        if self.is_omitted('criteria'):
            self._namespace.criteria = [self._default_criterium]


    # TODO: Methods to get indices and items as separate lists

    @QueueCommand.wrap
    def execute(self):
        if not self._indices:
            self.status = "Edited nothing"
        else:
            itemclass = self.queue.itemclass
            old = self.queue.items(*self._indices)
            new = self._ui.edit_items(itemclass, *old)
            self.queue.replace(self._indices, new)
            status = f"Edited {self.count(new)}"
            self.status = status


# Special case versions of EditCommand to edit just the top item or the whole
# queue. In the shell you'd just type "edit" or "edit 1-" but this is convenient
# in curses.

class EditCommand(EditorCommandBase):

    name = "edit"
    key = "e"
    _default_criterium = 1

class EditAllCommand(EditorCommandBase):

    name = 'manage'
    key = 'm'
    _default_criterium = "1-"
