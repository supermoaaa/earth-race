from weakref import proxy

class weakMethod(object):
    """A callable object. Takes one argument to init: 'object.method'.
    Once created, call this object -- MyWeakMethod() --
    and pass args/kwargs as you normally would.
    It's usefull to prevent bug with cyclic reference.
    """
    def __init__(self, object_dot_method):
        self.target = proxy(object_dot_method.__self__)
        self.method = proxy(object_dot_method.__func__)

    def __call__(self, *args, **kwargs):
        """Call the method with args and kwargs as needed."""
        return self.method(self.target, *args, **kwargs)
