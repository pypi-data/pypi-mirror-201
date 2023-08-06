# Provide a decorator to wrap a method so that it's called within the inherited
# version of that method.
#
# Example of use:
#
# class Parent(SuperWrapper):
#     def execute(self, method, *args, **kwargs):
#         print(f"Parent execute before")
#         method(self, *args, **kwargs)
#         print(f"Parent execute after")
#
# class InBetween(Parent):
#     @Parent.wrap
#     def execute(self, method, *args, **kwargs):
#         print(f"IB execute before")
#         method(self, *args, **kwargs)
#         print(f"IB execute after")
#
# class NewChild(InBetween):
#     @InBetween.wrap
#     def execute(self, name):
#         print(f"Hello {name}")
#
# c = NewChild()
# c.execute("Jane")


class SuperWrapper:
    @classmethod
    def wrap(parent_class, method):
        def wrapper(self, *args, **kwargs):
            parent_method = getattr(parent_class, method.__name__)
            return parent_method(self, method, *args, **kwargs)
        return wrapper
