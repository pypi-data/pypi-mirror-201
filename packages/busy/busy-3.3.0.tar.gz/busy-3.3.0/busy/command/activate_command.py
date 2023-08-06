from ..command.command import TodoCommand
from busy.util import date_util


# The Activate command is unusal because any criteria apply to the plans queue,
# not the main tasks queue.


def is_today_or_earlier(plan):
    return plan.date <= date_util.today()

class ActivateCommand(TodoCommand):

    name = 'activate'
    key = 'c'


    # Change in this version: "today" is the default if no criteria are given,
    # not a specific option.

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        self._add_criteria_arg(parser)
        self._add_confirmation_arg(parser)


    def clean_args(self):
        super().clean_args()
        self._ui.output('\n'.join(self._strings))
        self.confirm(f"Activate {self.count()}")


    # Indices behave differently, because they apply to the plans queue. We're
    # also going to do the defaulting here.
    #
    # TODO: Create a simpler way to handle the confirmation on another queue.

    @property
    def _indices(self):
        if not hasattr(self, '_indices_'):
            if self.is_omitted('criteria'):
                indices = self.queue.plans.indices(is_today_or_earlier)
                self._indices_ = indices
            else:
                self._indices_ = self.queue.plans.select(*self._criteria)
        return self._indices_

    @property
    def _strings(self):
        if not hasattr(self, '_strings_'):
            self._strings_ = self.queue.plans.strings(*self._indices)
        return self._strings_


    @TodoCommand.wrap
    def execute(self):
        if not self._indices:
            self.status = "Activated nothing"
        elif not self._namespace.yes:
            self.status = "Activate command canceled"
        else:
            activated = self.queue.activate(*self._indices)
            self.status = f"Activated {self.count(activated)}"
