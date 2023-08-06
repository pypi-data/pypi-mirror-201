# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0212,R0201,R0902,W0613,W0703,E0402,W0201,R0903


'handler'


import inspect
import queue
import ssl
import threading


from opb.objects import Default, Object
from opb.threads import launch


def __dir__():
    return (
            'Client',
            'Command',
            'Error',
            'Event',
            'Handler',
            'Listens',
            'command',
            'parse',
            'scan'
           )


__all__ = __dir__()


class Error(Object):

    errors = []

    @staticmethod
    def handle(ex):
        exc = ex.with_traceback(ex.__traceback__)
        Error.errors.append(exc)


class Handler(Object):

    def __init__(self):
        Object.__init__(self)
        self.cbs = Object()
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        self.register('command', self.handle)

    def dispatch(self, func, evt):
        try:
            func(evt)
        except Exception as ex:
            exc = ex.with_traceback(ex.__traceback__)
            Error.errors.append(exc)
            evt.ready()

    def event(self, txt):
        msg = Event()
        msg.type = 'command'
        msg.orig = repr(self)
        msg.parse(txt)
        return msg

    def handle(self, evt):
        func = getattr(self.cbs, evt.type, None)
        if func:
            evt._thr = launch(self.dispatch, func, evt, name=evt.cmd)
        return evt

    def loop(self):
        while not self.stopped.is_set():
            try:
                self.handle(self.poll())
            except (ssl.SSLError, EOFError, KeyboardInterrupt) as ex:
                Error.handle(ex)
                self.restart()

    def one(self, txt):
        return self.handle(self.event(txt))

    def poll(self):
        return self.queue.get()

    def put(self, evt):
        self.queue.put_nowait(evt)

    def register(self, cmd, func):
        setattr(self.cbs, cmd, func)

    def restart(self):
        self.stop()
        self.start()

    def start(self):
        launch(self.loop)

    def stop(self):
        self.stopped.set()
        self.queue.put_nowait(None)


class Command(Object):

    cmds = Object()

    @staticmethod
    def add(cmd, func):
        setattr(Command.cmds, cmd, func)

    @staticmethod
    def handle(evt):
        evt.parse(evt.txt)
        func = getattr(Command.cmds, evt.cmd, None)
        if func:
            try:
                func(evt)
                evt.show()
            except Exception as ex:
                Error.handle(ex)
        evt.ready()
        return evt


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        Listens.add(self)
        self.register('command', Command.handle)

    def announce(self, txt):
        self.raw(txt)

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)


class Event(Default):

    __slots__ = ('_ready', '_thr')

    def __init__(self, *args, **kwargs):
        Default.__init__(self, *args, **kwargs)
        self._ready = threading.Event()
        self._thr = None
        self.args = []
        self.gets = Default()
        self.orig = None
        self.result = []
        self.sets = Default()
        self.skip = Default()

    def parse(self, txt):
        self.otxt = txt
        spl = self.otxt.split()
        args = []
        _nr = -1
        for word in spl:
            if word.startswith('-'):
                try:
                    self.index = int(word[1:])
                except ValueError:
                    self.opts = self.opts + word[1:2]
                continue
            try:
                key, value = word.split('==')
                if value.endswith('-'):
                    value = value[:-1]
                    setattr(self.skip, value, '')
                setattr(self.gets, key, value)
                continue
            except ValueError:
                pass
            try:
                key, value = word.split('=')
                setattr(self.sets, key, value)
                continue
            except ValueError:
                pass
            _nr += 1
            if _nr == 0:
                self.cmd = word
                continue
            args.append(word)
        if args:
            self.args = args
            self.rest = ' '.join(args)
            self.txt = self.cmd + ' ' + self.rest
        else:
            self.txt = self.cmd

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        for txt in self.result:
            Listens.say(self.orig, txt, self.channel)

    def wait(self):
        if self._thr:
            self._thr.join()
        self._ready.wait()
        return self._result


class Listens(Object):

    objs = []

    @staticmethod
    def add(obj):
        Listens.objs.append(obj)

    @staticmethod
    def announce(txt):
        for obj in Listens.objs:
            obj.announce(txt)

    @staticmethod
    def byorig(orig):
        for obj in Listens.objs:
            if repr(obj) == orig:
                return obj
        return None

    @staticmethod
    def say(orig, txt, channel=None):
        bot = Listens.byorig(orig)
        if bot:
            if channel:
                bot.say(channel, txt)
            else:
                bot.raw(txt)


def command(cli, txt):
    evt = cli.event(txt)
    Command.handle(evt)
    evt.ready()
    return evt


def parse(txt):
    cfg = Event()
    cfg.parse(txt)
    if "v" in cfg.opts:
        cfg.verbose = True
    if "mod" in cfg.sets:
        cfg.mod = cfg.sets.mod
    return cfg


def scan(mod):
    for _key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if 'event' in cmd.__code__.co_varnames:
            Command.add(cmd.__name__, cmd)
