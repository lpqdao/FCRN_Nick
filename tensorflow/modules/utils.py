# ===========
#  Libraries
# ===========
from sys import getsizeof, stderr
from itertools import chain
from collections import deque


# ===========
#  Functions
# ===========
def total_size(o, handlers=None, verbose=False):
    """Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    """

    if handlers is None:
        handlers = {}

    def dict_handler(d):
        return chain.from_iterable(d.items())

    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                    }
    all_handlers.update(handlers)  # user handlers take precedence
    seen = set()  # track which object id's have already been seen
    default_size = getsizeof(0)  # estimate sizeof object without __sizeof__

    def sizeof(var):
        if id(var) in seen:  # do not double count the same object
            return 0
        seen.add(id(var))
        s = getsizeof(var, default_size)

        if verbose:
            print(s, type(var), repr(var), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(var, typ):
                # noinspection PyCallingNonCallable
                s += sum(map(sizeof, handler(var)))
                break
        return s

    return sizeof(o)
