# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,E0402


'status'


import io
import traceback


from opb.handler import Error, Listens
from opb.objects import prt


def err(event):
    for ex in Error.errors:
        stream = io.StringIO(traceback.print_exception(type(ex), ex, ex.__traceback__))
        for line in stream.readlines():
            event.reply(line)


def sts(event):
    for bot in Listens.objs:
        if 'state' in dir(bot):
            event.reply(prt(bot.state, skip='lastline'))
