# This file is placed in the Public Domain.
# pylint: disable=C0116,E0401


"introspection"


import importlib
import inspect
import os


from opb.handler import Command
from opb.utility import spl


def __dir__():
    return (
            'importer',
            'initer',
            'scan',
            'scandir',
            'scanpkg'
           )


def doimport(name, path):
    mod = None
    spec = importlib.util.spec_from_file_location(name, path)
    if spec:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    return mod


def include(txt, vals):
    for val in vals:
        if val in txt:
            return True
    return False


def importer(name, path):
    mod = doimport(name, path)
    scan(mod)
    return mod


def starter(mname, path=None):
    mod = doimport(mname, path)
    if "start" in dir(mod):
        mod.start()
    return mod


def listmods(path):
    return sorted([x[:-3] for x in os.listdir(path) if not x.startswith("__")])


def scan(mod):
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        names = cmd.__code__.co_varnames
        if "event" in names:
            Command.add(cmd.__name__, cmd)


def scanpkg(pkg, func, mods=None, doall=False):
    path = pkg.__path__[0]
    return scandir(path, func, mods, doall)


def scandir(pth, func, mods=None, doall=False):
    pname = ".".join(pth.split(os.sep)[-2:])
    if mods is None:
        mods = []
    else:
        mods = spl(mods)
    res = []
    if not os.path.exists(pth):
        return res
    for fnm in os.listdir(pth):
        if fnm.endswith("~") or fnm.startswith("__"):
            continue
        if not doall and not include(fnm, mods):
            continue
        mname = "%s.%s" % (pname, fnm.split(os.sep)[-1][:-3])
        path2 = os.path.join(pth, fnm)
        res.append(func(mname, path2))
    return res
