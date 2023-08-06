# Tihs file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,E0402


"persistence"


import os
import pathlib
import time
import _thread


from opb.objects import Object, dump, load, kind, search, update


def __dir__():
    return (
            'Persist',
            'cdir',
            'last',
            'find',
            'read',
            'setwd',
            'write'
           )


__all__ = __dir__()


disklock = _thread.allocate_lock()


class Persist(Object):

    workdir = os.path.expanduser("~/.opb")


def cdir(pth) -> None:
    if not pth.endswith(os.sep):
        pth = os.path.dirname(pth)
    pth = pathlib.Path(pth)
    os.makedirs(pth, exist_ok=True)


def files() -> []:
    return os.listdir(os.path.join(Persist.workdir, "store"))


def fns(match) -> []:
    assert Persist.workdir
    dname = ''
    lst = match.lower().split(".")[-1]
    for rootdir, dirs, _files in os.walk(Persist.workdir, topdown=False):
        if dirs:
            dname = sorted(dirs)[-1]
            if dname.count('-') == 2:
                ddd = os.path.join(rootdir, dname)
                fls = sorted(os.listdir(ddd))
                if fls:
                    path2 = os.path.join(ddd, fls[-1])
                    spl = strip(path2).split(os.sep)[0]
                    if lst in spl.lower().split(".")[-1]:
                        yield strip(path2)


def hook(otp) -> Object:
    obj = Object()
    read(obj, otp)
    return obj


def path(pth) -> str:
    return os.path.join(Persist.workdir, 'store', pth)


def read(obj, pth) -> None:
    pth = path(pth)
    with disklock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            data = load(ofile)
            update(obj, data)
    obj.__oid__ = strip(pth)


def setwd(pth) -> None:
    Persist.workdir = pth


def strip(pth) -> str:
    return os.sep.join(pth.split(os.sep)[-4:])


def write(obj) -> str:
    pth = path(obj.__oid__)
    cdir(pth)
    with disklock:
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile)
    return strip(pth)


def find(match, selector=None) -> []:
    if selector is None:
        selector = {}
    for fnm in fns(match):
        obj = hook(fnm)
        if '__deleted__' in obj:
            continue
        if selector and not search(obj, selector):
            continue
        yield obj


def last(obj, selector=None) -> None:
    if selector is None:
        selector = {}
    result = sorted(
                    find(kind(obj), selector),
                    key=lambda x: fntime(x.__oid__)
                   )
    if result:
        inp = result[-1]
        update(obj, inp)
        obj.__oid__ = inp.__oid__
    return obj.__oid__


def fntime(daystr):
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    tme = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        tme += float('.' + rest)
    else:
        tme = 0
    return tme
