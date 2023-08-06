# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,E0402


"list of bots"


from opb.handler import Listens
from opb.objects import kind


def __dir__():
    return (
            'flt',
           )


__all__ = __dir__()


def flt(event):
    try:
        index = int(event.args[0])
        event.reply(Listens.objs[index])
        return
    except (KeyError, TypeError, IndexError, ValueError):
        pass
    event.reply(' | '.join([kind(obj) for obj in Listens.objs]))
