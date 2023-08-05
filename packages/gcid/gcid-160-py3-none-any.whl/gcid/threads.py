# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0613,E0402


'threads'


import queue


from functools import wraps
from threading import Thread as BasicThread


def __dir__():
    return (
            'Thread',
            'launch',
            'threaded'
           )


__all__ = __dir__()


class Thread(BasicThread):

    def __init__(self, func, thrname, *args, daemon=True):
        super().__init__(None, self.run, thrname, (), {}, daemon=daemon)
        self._result = None
        self.name = thrname or str(func).split()[2]
        self.queue = queue.Queue()
        self.queue.put_nowait((func, args))
        self.sleep = None

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def join(self, timeout=None):
        super().join(timeout)
        return self._result

    def run(self):
        func, args = self.queue.get()
        self._result = func(*args)


def launch(func, *args, **kwargs):
    name = kwargs.get('name', '')
    thr = Thread(func, name, *args)
    thr.start()
    return thr


def threaded(func, *args, **kwargs):

    @wraps(func)
    def threadedfunc(*args, **kwargs):
        thr = launch(func, *args, **kwargs)
        if args:
            args[0].__thr__ = thr
        return thr

    return threadedfunc
