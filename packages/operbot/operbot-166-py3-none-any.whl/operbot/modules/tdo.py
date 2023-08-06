# This file is placed in the Public Domain.
# pylint: disable=C0103,C0115,C0116,R0903,E0402


'todo'


import time


from ..objects import Object
from ..persist import find, fntime, write


from .utility import elapsed


class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


def dne(event):
    if not event.args:
        return
    selector = {'txt': event.args[0]}
    for obj in find('todo', selector):
        obj.__deleted__ = True
        write(obj)
        event.reply('ok')
        break


def tdo(event):
    if not event.rest:
        nr = 0
        for obj in find('todo'):
            event.reply('%s %s %s' % (
                                      nr,
                                      obj.txt,
                                      elapsed(time.time()-fntime(obj.__oid__))))
            nr += 1
        if not nr:
            event.reply("nothing todo")
        return
    o = Todo()
    o.txt = event.rest
    write(o)
    event.reply('ok')
