# This file is placed in the Public Domain.
# pylint: disable=C0116,E0402


'command'


from opb.handler import Command


def __dir__():
    return (
            'cmd',
           )


def cmd(event):
    event.reply(','.join(sorted(Command.cmds)))
