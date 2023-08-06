# A terminal-based UI uses Curses, which offers one-key access to most common
# operations.
#
# The terminal has 3 regions, implemented as curses window objects. The regions
# are organized top-to-bottom with a 1-row gap between them. There is also a
# 1-row/1-column gap around the outside of the main terminal window containing
# the regions.
#
# Status region (_statuswin) - 6 lines at the top. Current queue name, current
# task, some blank space, status of the most recent operation, and input prompt
# for the main command.
#
# List region (_listwin) - Takes up the space between the other two regions.
# Shows mostly lists of tasks for confirmation and/or management.
#
# Edit region (_editwin) - 2 lines at the bottom. Used for editing of individual
# task descriptions, such as when adding a new task to the queue.


import curses
from argparse import Namespace
from string import capwords
from time import sleep

from busy.ui.ui import TerminalUI
from busy.ui.ui import UserCancelError
from busy.ui.ui import Prompt
from busy.ui.ui import Chooser


class CursesUI(TerminalUI):  # pragma: nocover

    name = "curses"

    def start(self):
        self._mode = "WORK"
        # Set up the main prompt once for simplicity
        # keynames = self.handler.get_command_values('key', 'name')
        # keynames.add(('q', 'quit'))
        # skeynames = sorted(keynames, key=lambda kn: kn[1])
        # self._main_prompt = Prompt(choices=skeynames)

        # Set up the main command chooser
        chooser = Chooser()
        commands = self.handler.get_commands('key')
        scommands = sorted(commands, key=lambda c:c.name)
        for command in scommands:
            chooser.add_choice(
                keys=[command.key],
                words=[command.name],
                action=command
            )
        chooser.add_choice(keys=['q'], words=['quit'])
        self._command_prompt = chooser

        curses.wrapper(self.term_loop)

    def output(self, intro=""):
        self._descwin.clear()
        self._descwin.addstr(intro)
        self._descwin.refresh()

    def write_prompt(self, prompt):
        """
        Output the prompt with underlines to the window.
        """
        window = self._statuswin
        if prompt.intro:
            window.addstr(prompt.intro + " ", curses.color_pair(3))
        if prompt.default:
            window.addstr(f"[{prompt.default}] ", curses.color_pair(3))
        for choice in prompt.choices:  # TODO: Deal with raw prompt case
            if choice.word==prompt.default:
                continue
            pre, it, post = choice.word.partition(choice.key)
            window.addstr(pre, curses.color_pair(3))
            window.addstr(it, curses.A_UNDERLINE + curses.color_pair(3))
            window.addstr(post + " ", curses.color_pair(3))
        window.addstr("--> ", curses.color_pair(3))


    # TODO: Use a better editing component
    #
    # NOTE: get_string assumes that everything has been cleared and we are in
    # the right place.

    def get_string(self, intro, default=""):
        prompt = Prompt(intro=intro, default=default)
        self._update_status(prompt)
        curses.echo()
        try:
            string = self._statuswin.getstr()
        except KeyboardInterrupt:
            raise UserCancelError
        value = string.decode() or default
        curses.noecho()
        return value

    def get_option(self, chooser):
        """Get a 1-keystroke choice from the user"""
        self._update_status(chooser)
        key = self._get_key()
        return chooser.choice_by_key(key)
    
    def term_loop(self, fullwin):
        self._queue_name = "tasks"
        curses.init_color(curses.COLOR_BLACK, 200, 200, 200)
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        h, w = fullwin.getmaxyx()
        self._statuswin = curses.newwin(5, w-2, 1, 1)
        self._descwin = curses.newwin(h-8, w-2, 7, 1)
        self._editwin = curses.newwin(1, w-2, h-2, 1)
        self._status = "Welcome to Busy!"
        list = ""
        cursor = 0
        while True:
            self.output()
            self._update_status(self._command_prompt)
            try:
                key = self._get_key()
            except UserCancelError:
                break
            if key == "q":
                break
            command = self.handler.get_command('key', key, ui=self, \
                    root=self.handler.root, queue_name=self._queue_name)
            if not command:
                self._status = f"Invalid command {key}"
                continue
            command_name = capwords(command.name)
            self._status = f"{command_name} in progress"
            self._update_status()
            try:
                result = command.execute()
                self._status = command.status or ""
                if hasattr(command, 'queue_name'):
                    self._queue_name = command.queue_name
            except UserCancelError:
                self._status = f"{command_name} command canceled"

    def _update_status(self, prompt=None):
        queue = self.handler.root.get_queue(self._queue_name)
        self._statuswin.clear()
        self._statuswin.move(0, 0)
        self._statuswin.addstr("Queue: ", curses.color_pair(1))
        self._statuswin.addstr(capwords(self._queue_name), curses.A_BOLD)
        self._statuswin.move(1, 0)
        self._statuswin.addstr("Top:   ", curses.color_pair(1))
        self._statuswin.addstr(str(queue.top()) or '', curses.A_BOLD)
        self._statuswin.move(3, 0)
        self._statuswin.addstr(self._status, curses.color_pair(2))
        self._statuswin.move(4, 0)
        if prompt:
            self.write_prompt(prompt)
        cursor = self._statuswin.getyx()
        self._statuswin.refresh()
        self._statuswin.move(*cursor)

    # Convenience method to get one keystroke from the user.
    #     
    def _get_key(self):
        try:
            key = self._statuswin.getkey()
        except (KeyboardInterrupt, curses.error):
            raise UserCancelError
        # self._statuswin.addstr(key)
        return key


    # def listmode(self):
    #     length = len(list.splitlines())
    #     if length:
    #         listpad = curses.newpad(length, curses.COLS)
    #         listpad.addstr(list)
    #         self.listmode = True
    #         listpad.move(cursor, 0)
    #         listpad.addstr(">")
    #         listpad.refresh(0, 0, 5, 0, curses.LINES - 5, curses.COLS)
    #     if self.listmode:
    #         if key == "KEY_UP" and cursor > 0:
    #             cursor = cursor - 1
    #         if key == "KEY_DOWN" and cursor < length:
    #             cursor = cursor + 1
