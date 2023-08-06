# Mark a task as finished by moving it to the done queue.

from ..command.command import TodoCommand
from busy.util.date_util import today
from busy.util.date_util import relative_date

class FinishCommand(TodoCommand):

    name = 'finish'
    key = 'n'


    # TODO: Add an option for the date, including e.g. "yesterday"

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        parser.add_argument('--timing', '--on')
        self._add_confirmation_arg(parser)
        self._add_criteria_arg(parser)


    # TODO: Use relative if a date is specified (for now we are just using today
    # in all cases).

    def clean_args(self):
        super().clean_args()
        if self.is_omitted('criteria'):
            self._namespace.criteria = [1]
        self._ui.output('\n'.join(self._strings))
        if self.is_omitted('timing'):
            self._namespace.timing = "today"
        self.confirm(f"Finish {self.count()} on {self._date}")
        # TODO: Allow for changing the date on "other"


    @property
    def _date(self):
        if not hasattr(self, '_date_'):
            self._date_ = relative_date(self._namespace.timing)
        return self._date_

    # TODO: Move the listing and confirmation into clean_args.
    # TODO: Shouldn't self._criteria reference self._namespace?

    @TodoCommand.wrap
    def execute(self):
        if not self._indices:
            self.status = "Finished nothing"
        elif not self._namespace.yes:
            self.status = "Finish operation unconfirmed"
        else:
            finished, added, deferred = self.queue.finish(*self._indices, date=self._date)
            status = f"Finished {self.count(finished)}"
            if added:
                status += f" // Added {str(len(added))}"
            if deferred:
                status += f" // Repeated {str(len(deferred))}"
            self.status = status
