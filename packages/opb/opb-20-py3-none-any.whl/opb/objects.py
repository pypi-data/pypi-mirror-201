# This file is placed in the Public Domain.
# pylint: disable=C0112,C0115,C0116,R0903,E0402


"a clean namespace"


import datetime
import json
import os
import uuid
import _thread


from json import JSONDecoder, JSONEncoder


def __dir__():
    return (
            'Default',
            'Object',
            'items',
            'keys',
            'kind',
            'prt',
            'search',
            'update',
            'values',
           )


__all__ = __dir__()


lock = _thread.allocate_lock()


class Object:

    __slots__ = ('__dict__', '__oid__')

    def __init__(self, *args, **kwargs):
        self.__oid__ = ident(self)
        if args:
            val = args[0]
            if isinstance(val, list):
                update(self, dict(val))
            elif isinstance(val, zip):
                update(self, dict(val))
            elif isinstance(val, dict):
                update(self, val)
            elif isinstance(val, Object):
                update(self, vars(val))
        if kwargs:
            self.__dict__.update(kwargs)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


def ident(obj):
    return os.path.join(
                        kind(obj),
                        str(uuid.uuid4().hex),
                        os.sep.join(str(datetime.datetime.now()).split()),
                       )


def items(obj) -> []:
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj) -> []:
    return obj.__dict__.keys()


def kind(obj) -> str:
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = obj.__name__
    return kin


def prt(obj, args="", skip="", plain=False):
    res = []
    keyz = []
    if "," in args:
        keyz = args.split(",")
    if not keyz:
        keyz = keys(obj)
    for key in sorted(keyz):
        if key.startswith("_"):
            continue
        if skip:
            skips = skip.split(",")
            if key in skips:
                continue
        value = getattr(obj, key, None)
        if not value:
            continue
        if " object at " in str(value):
            continue
        txt = ""
        if plain:
            value = str(value)
            txt = f'{value}'
        elif isinstance(value, str) and len(value.split()) >= 2:
            txt = f'{key}="{value}"'
        else:
            txt = f'{key}={value}'
        res.append(txt)
    txt = " ".join(res)
    return txt.strip()


def search(obj, selector) -> bool:
    res = False
    select = Object(selector)
    for key, value in items(select):
        try:
            val = getattr(obj, key)
        except AttributeError:
            continue
        if str(value) in str(val):
            res = True
            break
    return res


def update(obj, data) -> None:
    for key, value in items(data):
        setattr(obj, key, value)


def values(obj) -> []:
    return obj.__dict__.values()


class Default(Object):

    __slots__ = ("__default__",)

    def __init__(self, *args, **kwargs):
        Object.__init__(self, *args, **kwargs)
        self.__default__ = ""

    def __getattr__(self, key):
        return self.__dict__.get(key, self.__default__)


class ObjectDecoder(JSONDecoder):

    errors = []

    def __init__(self):
        ""
        JSONDecoder.__init__(self)

    def decode(self, s, _w=None) -> Object:
        ""
        val = JSONDecoder.decode(self, s)
        if not val:
            val = {}
        return Object(val)

    def raw_decode(self, s, idx=0) -> (int, Object):
        ""
        return JSONDecoder.raw_decode(self, s, idx)


def load(fpt, *args, **kw) -> Object:
    return json.load(fpt, *args, cls=ObjectDecoder, **kw)


def loads(string, *args, **kw) -> Object:
    return json.loads(string, *args, cls=ObjectDecoder, **kw)


class ObjectEncoder(JSONEncoder):

    def __init__(self, *args, **kw):
        ""
        JSONEncoder.__init__(self, *args, **kw)

    def default(self, o) -> str:
        ""
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        if isinstance(o,
                      (type(str), type(True), type(False),
                       type(int), type(float))
                     ):
            return str(o)
        try:
            return JSONEncoder.default(self, o)
        except TypeError:
            return str(o)

    def encode(self, o) -> str:
        ""
        return JSONEncoder.encode(self, o)

    def iterencode(self, o, _one_shot=False) -> str:
        ""
        return JSONEncoder.iterencode(self, o, _one_shot)


def dump(*args, **kw) -> None:
    kw["cls"] = ObjectEncoder
    return json.dump(*args, **kw)


def dumps(*args, **kw) -> str:
    kw["cls"] = ObjectEncoder
    return json.dumps(*args, **kw)
