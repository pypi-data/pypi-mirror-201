# A class family is a set of class definitions that use single inheritance (each
# subclass inherits from only one parent) and often multiple inheritance
# (subclasses can inherit from subclasses). So it's a hierarchy of classes, with
# one super-parent at the top.
#
# We offer a way for members of the family to declare themselves simply by
# living in the right package location. Then those classes can be instantiated
# using keys or names, without having to be specifically called. The members act
# independently of each other.
#
# What we get, after importing everything and loading it all, is essentially a
# little database of classes, where class-level properties become keys for
# looking up member classes. So, for example, we can have a family of commands,
# and use a command string to look up the right command.
#
# Ultimately, the super-parent of the family -- the class at the top of the
# hierarchy -- holds the database, actually a list, in the property called
# "family". So that class can be queried to find appropriate family member
# classes or instances thereof.
#
# This utility provides functions for importing family members, loading the
# "families" property of the super-parent, and querying the family.
#
# In the process of loading and querying the class family, we need to *avoid*
# inheritance of attributes. There might be abstract intermediary classes that
# don't want to play. So we use __dict__ to ensure we're only seeing the
# atttributes that are defined on that specific class.


from pathlib import Path
from importlib import import_module
from re import match
from inspect import getmodule


class ClassFamily:


    # Return an attribute of this specific class, not inherited.

    @classmethod
    def get_member_attr(self, attribute):
        if attribute in self.__dict__:
            return self.__dict__[attribute]


    # True or False: This class has all the attributes provided. Return True if
    # no attributes provided. Use __subclasses__ so we only look at direct
    # descendents, and __dict__ so we only look at attributes defined here (not
    # inherited).

    @classmethod
    def has_member_attrs(self, *attributes):

        # Do I have all the attributes?
        matches = [a in self.__dict__ for a in attributes]

        # Python's all() function returns True if the list is empty. So we kill
        # two birds with one stone here - get a hit if there are no attributes,
        # and avoid the empty-matches problem.
        return all(matches + list(attributes))


    # Return a set of myself and all my descendents that have certain
    # attributes. If no attribute names are provided, return the entire family.

    @classmethod
    def family_members(self, *attributes):

        # Put myself into a set if I qualify
        hits = {self} if self.has_member_attrs(*attributes) else set()

        # Go through my subclasses
        for kid in self.family_children():

            # Call the same function on each subclass
            hits |= kid.family_members(*attributes)
        
        # Send it back
        return hits


    # Return a set of tuples of all the values of a specific attribute that
    # exist in the family. The set avoids repetition of values in the result. We
    # recognize that the method name has cultural implications, and we find that
    # fact ironic and funny.

    @classmethod
    def family_attrs(self, *attributes):

        # Put myself into a set if I qualify
        if self.has_member_attrs(*attributes):
            values = {tuple(self.get_member_attr(a) for a in attributes)}
        else:
            values = set()

        # Go through my subclasses
        for kid in self.family_children():

            # Call the same function on each subclass
            values |= kid.family_attrs(*attributes)
        
        # Send it back
        return values


        # Start with an empty set
        result = set()

        # If I have the provided attribute, get its value. Use __dict__ rather
        # than hasattr() and getattr() to refer only to myself, rather than
        # inherited attributes.
        for attribute in attributes:
            if attribute in self.__dict__:
                result |= {self.__dict__[attribute]}

        # Go through my subclasses, collecting their values
        for kid in self.family_children():
            result |=  kid.family_values(attribute)
        
        # Return it
        return result


    # Return a specific family member that has a specified value of an
    # attribute. Assume that there is only one, so return it as soon as it's
    # found.

    @classmethod
    def family_member(self, attribute, value):

        # See if I qualify, and if so, return myself. Use __dict__ rather than
        # hasattr() and getattr() to refer only to myself, rather than inherited
        # attributes.
        if attribute in self.__dict__:
            if self.__dict__[attribute] == value:
                return self
            
        # Go through the subclasses, doing the same. The return statement will
        # exit the loop, so we get out as soon as we find one, without having to
        # evaluate others.
        for kid in self.family_children():
            found = kid.family_member(attribute, value)
            if found:
                return found


    # Import the whole family, so they show up as subclasses. Then return this
    # classes subclasses. This obviates the need to import everything at
    # initialization. It happens when needed, and only once.  Family members
    # must be in modules (files) in the same directory as the parent (me).
    # Furthermore, all the files in that directory will be imported. The only
    # exception is a file with the same name as myself, to avoid circular
    # imports. This is a private method, intended to be called when needed.

    @classmethod
    def family_children(self):

        # We only need to import the family once
        if not hasattr(self, '_family_imported'):

            # Find the location of the directory and the name of the module
            module = getmodule(self)
            directory = Path(module.__file__).parent
            module_name = module.__package__

            # Go through the directory and import everything into the module
            for import_file in directory.iterdir():
                if match(r'^[^_].*\.py$', import_file.name):
                    import_module(f'{module_name}.{import_file.stem}')

            # Prevent it from needing to run again
            self._family_imported = True

        # Return the subclasses (children)
        return self.__subclasses__()
    