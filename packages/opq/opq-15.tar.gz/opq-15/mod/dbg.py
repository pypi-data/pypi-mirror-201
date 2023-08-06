# This file is placed in the Public Domain.
# pylint: disable=C0114,C0116


def __dir__():
    return (
            'dbg',
           )


def dbg(event):
    raise Exception('debug!')
