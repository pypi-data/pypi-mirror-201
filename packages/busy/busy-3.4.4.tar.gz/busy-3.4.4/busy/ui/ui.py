# Abstract classes for UIs. The idea here is to allow many different user
# interfaces (shell, curses, Slack, etc) to drive the same data model without
# the data model needing specific UI knowledge.
#
# The UI keeps a reference to the Handler. The Handler will bring a Command with
# it, and this is the main root command. In the case of a Shell-type UI, that is
# the command to be executed. In the case of an interactive UI, it's really just
# a placeholder; the UI will instantiate other commands as it proceeds. But the
# Handler won't know about those.
#
# Commands might call back to the UI for confirmations or arguments that are
# previously omitted, using the get_ methods.

#
# UI end classes must implement the following interface:
#
# __init__(handler): Takes the handler and hangs on to it. Implemented in the
# main base class.
#
# start(): No arguments. Actually performs the operation of the UI. It might be
# short running (in the case of a shell UI) or long-running (in the case of an
# interactive UI).
#
# output(intro=""): Output some multi-line text explaining an action, usually a
# list of items being acted upon.
#
# get_string(prompt, default=""): For arguments that are omitted, get a string
# from the user. The prompt is just a word (like "Description") telling the user
# what to input.
#
# get_confirmation(verb): For delete-oriented commands to
# confirm with the user before proceeding. Verb is what we're asking the user to
# confirm. Description can be multiple lines, as with get_string. Returns a
# boolean saying whether the action is confirmed.

import subprocess
from tempfile import NamedTemporaryFile
from pathlib import Path
import shutil
import os
import re
from io import StringIO
from dataclasses import dataclass, field
from enum import Enum

from busy.model.item import write_items
from busy.model.item import read_items
from busy.util.class_family import ClassFamily



@dataclass
class Choice:
    """One option of several"""

    keys:list[str] = field(default_factory=list)
    words:list[str] = field(default_factory=list)
    action:object = None

    @property
    def key(self):
        return self.keys[0]
    
    @property
    def word(self):
        return self.words[0]

    def hit_key(self, key):
        return key in self.keys

    def hit_word(self, word):
        return word in self.words
    
    def call(self, *args, **kwargs):
        if callable(self.action):
            return self.action(*args, **kwargs)


@dataclass
class Prompt:
    """Tell the user what kind of input to provide"""

    intro:str = ""
    default:str = ""
    choices:list = field(default_factory=list)


@dataclass
class Chooser(Prompt):
    """Hold a set of choices and get the result"""

    def add_choice(self, *args, **kwargs):
        choice = Choice(*args, **kwargs)
        self.choices.append(choice)

    def choice_by_key(self, key):
        chosenlist = [o.action for o in self.choices if o.hit_key(key)]
        return self._choose(chosenlist)

    def choice_by_word(self, word):
        chosenlist = [o.action for o in self.choices if o.hit_word(word)]
        return self._choose(chosenlist)

    def _choose(self, chosenlist):
        choice = next(iter(chosenlist), None)
        if callable(choice):
            return choice()
        else:
            return choice


class UI(ClassFamily):

    def __init__(self, handler=None):
        self.handler = handler

    def get_chooser(self, *args, **kwargs):
        """Return a chooser that can be set up with options"""
        return Chooser(*args, **kwargs)
    
    # TODO: Make start an abstract method
    def start(self):
        pass

    # TODO: Make get_option an abstract method
    def get_option(self, chooser:Chooser):
        """Get an option from a list from the user"""
        pass

    # TODO: Make get_string an abstract method
    def get_string(self, intro, default=""):
        """Get a string value from the user"""
        pass


# Terminal UIs include Shell and Curses, since both will rely on a
# terminal-based editor for the e.g. Manage command.

class TerminalUI(UI):

    # A convenience method to get a full textual prompt for a string input

    def full_prompt(self, prompt, default=None):
        if default:
            return f'{prompt} [{default}]: '
        else:
            return f'{prompt}: '


    def edit_items(self, itemclass, *items):
        commands = [['sensible-editor'], ['open', '-W']]
        with NamedTemporaryFile(mode="w+") as tempfile:
            write_items(tempfile, *items)
            tempfile.seek(0)
            command = [os.environ.get('EDITOR')]
            if not command[0] or not shutil.which(command[0]):
                iterator = (c for c in commands if shutil.which(c[0]))
                command = next(filter(None, iterator), None)
                if not command:
                    raise RuntimeError("A text editor at the $EDITOR environment variable is required")
            subprocess.run(command + [tempfile.name])
            tempfile.seek(0)
            new_items = read_items(tempfile, itemclass)
            return new_items


class UserCancelError(Exception):
    pass
