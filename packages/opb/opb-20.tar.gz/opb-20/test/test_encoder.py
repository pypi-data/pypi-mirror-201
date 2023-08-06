# This file is placed in the Public Domain.
# pylint: disable=C0114,C0115,C0116


"encoder tests"


import unittest


from opb.objects import Object, dumps


VALIDJSON = '{"test": "bla"}'


class TestEncoder(unittest.TestCase):


    def test_dumps(self):
        obj = Object()
        obj.test = "bla"
        self.assertEqual(dumps(obj), VALIDJSON)
