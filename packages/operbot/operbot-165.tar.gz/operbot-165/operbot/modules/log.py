# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,E0402


'log'


import time


from ..persist import find, fntime, write
from ..objects import Object


from .utility import elapsed


def __dir__():
    return (
            'Log',
            'log',
           )


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


def log(event):
    if not event.rest:
        nmr = 0
        for obj in find('log'):
            event.reply('%s %s %s' % (
                                      nmr,
                                      obj.txt,
                                      elapsed(time.time() - fntime(obj.__oid__)))
                                     )
            nmr += 1
        if not nmr:
            event.reply('log <txt>')
        return
    obj = Log()
    obj.txt = event.rest
    write(obj)
    event.reply('ok')
