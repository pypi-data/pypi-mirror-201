class SuperWrapper:
    @classmethod
    def wrap(parent_class, method):
        def wrapper(self, *args, **kwargs):
            parent_method = getattr(parent_class, method.__name__)
            parent_method(self, method, *args, **kwargs)
        return wrapper


class Parent(SuperWrapper):

    def execute(self, method, *args, **kwargs):
        print(f"Parent execute before")
        method(self, *args, **kwargs)
        print(f"Parent execute after")


class InBetween(Parent):

    @Parent.wrap
    def execute(self, method, *args, **kwargs):
        print(f"IB execute before")
        method(self, *args, **kwargs)
        print(f"IB execute after")

class NewChild(InBetween):

    @InBetween.wrap
    def execute(self, name):
        print(f"Hello {name}")

c = NewChild()
c.execute("Jane")

