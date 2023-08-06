#!/usr/bin/env python3
# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0212,E0402,E0401,R0201


'shell'


import atexit
import getpass
import os
import pwd
import readline
import rlcompleter
import sys
import termios
import time
import traceback


from opb.handler import Client, Error, command, parse
from opb.objects import Default, update
from opb.scanner import scanpkg, importer, starter


import opb.modules


def __dir__():
    return (
            'CLI',
            'Completer',
            'Console',
            'setcompleter',
            'daemon',
            'privileges',
            'waiter',
            'wrap'
           )


__all__ = __dir__()


Cfg = Default()
Cfg.debug = False
Cfg.name = "opb"


date = time.ctime(time.time()).replace('  ', ' ')
name = Cfg.name.upper()


def start():
    wrap(main)


class CLI(Client):

    def announce(self, txt):
        pass

    def raw(self, txt):
        print(txt)


class Console(CLI):

    def handle(self, evt):
        CLI.handle(self, evt)
        evt.wait()

    def poll(self):
        return self.event(input('> '))


class Completer(rlcompleter.Completer):

    def __init__(self, options):
        super().__init__()
        self.matches = []
        self.options = options

    def complete(self, text, state):
        if state == 0:
            if text:
                self.matches = [s for s in self.options if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
        try:
            return self.matches[state]
        except IndexError:
            return None


def setcompleter(optionlist):
    completer = Completer(optionlist)
    readline.set_completer(completer.complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))


def daemon():
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    os.umask(0)
    sis = open('/dev/null', 'r')
    os.dup2(sis.fileno(), sys.stdin.fileno())
    sos = open('/dev/null', 'a+')
    ses = open('/dev/null', 'a+')
    os.dup2(sos.fileno(), sys.stdout.fileno())
    os.dup2(ses.fileno(), sys.stderr.fileno())


def privileges(username):
    if os.getuid() != 0:
        return
    try:
        pwnam = pwd.getpwnam(username)
    except KeyError:
        username = getpass.getuser()
        pwnam = pwd.getpwnam(username)
    os.setgroups([])
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


def waiter():
    got = []
    for ex in Error.errors:
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        got.append(ex)
    for exc in got:
        Error.errors.remove(exc)


def wrap(func):
    fds = sys.stdin.fileno()
    gotterm = True
    try:
        old = termios.tcgetattr(fds)
    except termios.error:
        gotterm = False
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        print("")
    finally:
        if gotterm:
            termios.tcsetattr(fds, termios.TCSADRAIN, old)


def main():
    dowait = False
    cfg = parse(' '.join(sys.argv[1:]))
    update(Cfg, cfg.sets)
    scanpkg(opb.modules, importer, doall=True)
    if cfg.txt:
        cli = CLI()
        command(cli, cfg.otxt)
    elif 'd' in cfg.opts:
        daemon()
        dowait = True
    elif 'c' in cfg.opts:
        print(f'{name} started {date}')
        csl = Console()
        csl.start()
        dowait = True
    if dowait:
        scanpkg(opb.modules, starter, Cfg.mod)
        while 1:
            time.sleep(1.0)


if __name__ == "__main__":
    start()
