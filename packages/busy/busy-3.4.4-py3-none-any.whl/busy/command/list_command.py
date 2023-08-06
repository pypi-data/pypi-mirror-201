from ..command.command import QueueCommand


class ListCommand(QueueCommand):

    name = 'list'
    # key = "l"

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        self._add_criteria_arg(parser)

    @QueueCommand.wrap
    def execute(self):
        listed = self.queue.list(*self._criteria)
        if len(listed) == 1:
            self.status = f"Listed 1 Item"
        elif listed:
            self.status = f"Listed {str(len(listed))} Items"
        else:
            self.status = "Listed nothing"
        fmtstring = "{0:>6}  " + self.queue.itemclass.listfmt
        return "\n".join([fmtstring.format(i, t) for i, t in listed])


