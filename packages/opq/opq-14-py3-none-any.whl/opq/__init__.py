# This file is placed in the Public Domain.
# pylint: disable=C0116,W0406,E0401,E0611,R0201


"functional programming with objects"


from . import clocked, handler, modules, objects, persist, threads
from .objects import Object, items, keys, kind, update, values
from .persist import Persist, find, last, read, write


NAME = "opq"


def __dir__():
    return (
            'Object',
            'Persist',
            'items',
            'keys',
            'kind',
            'read',
            'update',
            'values',
            'write'
           )


__all__ = __dir__()
