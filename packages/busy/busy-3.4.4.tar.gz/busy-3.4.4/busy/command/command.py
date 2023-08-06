# A Command class handles argparse stuff (ArgumentParser and Namespace) on
# behalf of a method somewhere in the model (i.e. on Queue) and returns text
# that can be used in a UI. A Command class rarely performs an actual operation.
#
# Command classes must have the following class-level properties:
#
# ui - Name of the UI associated with this Command. Default is 'shell', set in
# base class. Inside the command, self._ui refers to the UI object itself.
#
# name - Name of the command. Used in the original Shell UI and also as the name
# of the methods on the queue.
#
# Commands must implement the following methods:
#
# @classmethod set_parser(parser) - Receives an ArgumentParser (actually a
# subparser, but that's irrelevant here), adds arguments to it as appropriate
# for that command, and keeps a reference to it in self.parser.
#
# __init__(root, ui) - Receives the Root and UI; sets self._* for both.
# Implemented in the base class.
#
# execute(namespace) - Perform the command. It might use the namespace from the
# Handler, or it might accept a new Namespace, in the event of interactive UIs.
# The execute method is expected to set a property "status" with a one-line
# string description of what happened.
#
# A Command might implement the following methods:
#
# clean_args() - Examine the self._namespace and use the UI to request any
# args that are omitted. Tends to be command-specific.
#
# They might have the following class attributes:
#
# key - For the Curses UI. What key the user should press.
#
# TODO: Move the base class to __init__.py
# TODO: Make it an ABC

from argparse import Namespace

from busy.util.class_family import ClassFamily
from busy.util.super_wrapper import SuperWrapper

class Command(ClassFamily, SuperWrapper):

    ui = 'shell'

    @classmethod
    def set_parser(self, parser):
        self.parser = parser


    # Convenience method to add an argument to flag for confirmation in the
    # command line itself.

    @classmethod
    def _add_confirmation_arg(self, parser):
        parser.add_argument('--yes', action='store_true')


    # TODO: Get rid of namespace entirely, then use @dataclass

    def __init__(self, root=None, ui=None, namespace=None, **kwargs):
        self._root = root
        self._ui = ui
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])
        self.status = None

        # Temporary code until we remove namespace
        if namespace is None:
            namespace = Namespace()
        self._namespace = namespace
        if namespace:
            ns = vars(namespace)
            for key in ns:
                setattr(self, key, ns[key])


    # Actually perform the command. Designed for SuperWrapper.

    def execute(self, method, *args, **kwargs):
        self.clean_args()
        result = method(self, *args, **kwargs)
        return result


    # The clean_args method serves 3 purposes.
    # 
    # (1) If any arguments are missing from the command, ask the user to provide
    # them through the UI. For example, when adding a new item to a queue, if a
    # description is not yet provided, ask the user to provide one.
    # 
    # (2) This is where defaulting happens. Defaults should generally not be
    # applied in the model, but rather here in the command layer, closer to the
    # user.
    #
    # (3) Call for confirmation from the user (using is_confirmed) if
    # appropriate.
    #
    # The default is to do nothing, as this is essentially an abstract method
    # ripe for override.

    def clean_args(self):
        pass


    # Convenience method to find out whether an argument was omitted when the
    # Command was created. This will get shorter when we remove namespace
    # entirely. In fact, maybe it just goes away entirely. Technically, it's not
    # omitted if it's false.
    #
    # TODO: Rethink this

    def is_omitted(self, argument):
        if hasattr(self._namespace, argument):
            value = getattr(self._namespace, argument)
        elif hasattr(self, argument):
            value = getattr(self, argument)
        else:
            value = None
        if value == False:
            return False
        return not value


    # Convenience method to figure out whether the command is confirmed, either
    # in the original command or from the UI. Sets namespace.yes if confirmation
    # is complete, otherwise leaves it alone. Returns the confirmation object so
    # the other method can be executed.

    def confirm(self, verb, other_action=None):
        if self.is_omitted('yes') or not self._namespace.yes:
            chooser = self._ui.get_chooser(intro = f"{verb}?", default = "ok")
            chooser.add_choice(keys=['y','\n', ''], words=['ok'], action=True)
            chooser.add_choice(keys=['c'], words=['cancel'], action=False)
            if other_action:
                chooser.add_choice(keys=['o'], words=['other'], action=other_action)
            choice = self._ui.get_option(chooser)
            if type(choice) == bool:
                self._namespace.yes = choice
            return choice


# Abstract base command for commands that work with one queue. A QueueCommand
# knows the reference to the Queue, and takes care of loading and saving with
# the root. A QueueCommand subclass might implement:
#
# execute() - Call the actual method on the queue. This allows for
# specialized arguments passed into the method. If omitted, the default is to
# pass the criteria from the Namespace.

class QueueCommand(Command):

    default_queue = 'tasks'

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        parser.add_argument('--queue', dest='queue_name')

    # Convenience method used by some queue commands to add criteria as an
    # argument, to allow for the selection of items from the queue. Some queue
    # commands operate on the whole queue and don't require criteria.

    @classmethod
    def _add_criteria_arg(self, parser):
        parser.add_argument('criteria', action='store', nargs="*")


    # Set the queue if it isn't designated. Note this can't happen in argparse
    # because we might be called from a different kind of UI.

    def clean_args(self):
        super().clean_args()
        if self.is_omitted('queue_name'):
            self.queue_name = self.default_queue


    # Get the Queue object being acted on. Remember it the first time so it's
    # easy to get the next time.

    @property
    def queue(self):
        if not hasattr(self, '_queue'):
            self._queue = self._root.get_queue(self.queue_name)
        return self._queue


    # Many commands take criteria to get items from a queue. Here are shortcuts
    # to look up the indices and the strings only once.

    @property
    def _indices(self):
        if not hasattr(self, '_indices_'):
            self._indices_ = self.queue.indices(*self._criteria)
        return self._indices_

    @property
    def _strings(self):
        if not hasattr(self, '_strings_'):
            self._strings_ = self.queue.strings(*self._indices)
        return self._strings_

    # Queues contain methods with the same name as the commands, so we really
    # just need to get it and call it.

    @Command.wrap
    def execute(self, method, *args, **kwargs):
        result = method(self, *args, **kwargs)
        self._root.save()
        return result

    # The default, which works for many queue commands, is to pass the criteria
    # into the method. This never sets the status, so not useful?

    # def execute(self):
    #     method = getattr(self.queue, self.name)
    #     method(*self._namespace.criteria)


    # Convenience method to get the criteria from the namespace, including
    # handling the case when there is none provided

    @property
    def _criteria(self):
        if hasattr(self._namespace, 'criteria'):
            return self._namespace.criteria
        else:
            return []
        
    def count(self, items=None):
        """Return a friendly string count of some items"""
        if items is None:
            items = self._indices
        if len(items) == 1:
            return "1 item"
        if len(items) > 1:
            return str(len(items)) + " items"
        return "nothing"

# Commands that are specific to the task queue inherit here. Ideally we would
# verify that the queue being used is a TodoQueue, but we're going to rely on
# defaults and argparse for that now.

class TodoCommand(QueueCommand):


    # Make sure we're using the tasks queue. Think about whether the "default"
    # queue is the same as the "required" queue for todo operations.

    def clean_args(self):
        super().clean_args()
        if self.queue_name != self.default_queue:
            message = "Todo commands only operate on the "
            message += f"{self.default_queue} queue."
            raise RuntimeError(message)