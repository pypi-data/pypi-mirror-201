from ..command.command import Command


class CursesCommand(Command):

    name = 'curses'
    ui = 'curses'


    # The execute method might be generic to all interactive UIs.

    def execute(self):
        self._ui.start()
        print(f'Session complete: {self._ui.name}')

