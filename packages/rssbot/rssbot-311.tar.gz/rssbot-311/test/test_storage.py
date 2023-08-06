# This file is placed in the Public Domain.


import json
import os
import unittest


from rssbot.objects import Object
from rssbot.persist import Persist, path, write


import rssbot.persist


Persist.workdir = '.test'


ATTRS1 = (
          'Persist',
          'cdir',
          'find',
          'last',
          'read',
          'setwd',
          'write'
         )


class TestStorage(unittest.TestCase):

    def test_constructor(self):
        obj = Persist()
        self.assertTrue(type(obj), Persist)

    def test__class(self):
        obj = Persist()
        clz = obj.__class__()
        self.assertTrue('Persist' in str(type(clz)))

    def test_dirmodule(self):
        self.assertEqual(
                         dir(rssbot.persist),
                         list(ATTRS1)
                        )

    def test_module(self):
        self.assertTrue(Persist().__module__, 'rssbot.persist')

    def test_save(self):
        Persist.workdir = '.test'
        obj = Object()
        opath = write(obj)
        self.assertTrue(os.path.exists(path(opath)))
