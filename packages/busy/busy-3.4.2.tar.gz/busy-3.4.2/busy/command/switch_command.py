from busy.command.command import Command

# Switch to a different queue. Note this only works in interactive UIs; the
# shell UI has no state so it's essentially a no-op.

# TODO: Make SwitchCommand only work in stateful UIs

class SwitchCommand(Command):

    name = "switch"
    key = "w"

    def clean_args(self):
        self._new_queue_name = self._ui.get_string("Switch to queue", "tasks")
        self._new_queue = self._root.get_queue(self._new_queue_name)
        if self.is_omitted('yes'):
            if self._new_queue.count() == 0:
                self.confirm(f"Switch to empty queue {self._new_queue_name}")
            else:
                self._namespace.yes = True


    @Command.wrap
    def execute(self):
        if self._namespace.yes:
            self.queue_name = self._new_queue_name
            self.status = f"Switched to queue {self._new_queue_name}"
        else:
            self.status = "Switch operation canceled"

