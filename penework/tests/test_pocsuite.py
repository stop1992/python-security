#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 penework developers (http://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

# from penework import penework_cli
# from penework import penework_verify
# from penework import penework_attack
# from penework import penework_console

from penework_cli import modulePath
from lib.core.common import setPaths
from lib.core.data import paths

from nose.tools import assert_true


class TestPocsuiteBase(object):

    def test_penework_setpath(self):
        paths.PENEWORK_ROOT_PATH = modulePath()
        setPaths()
        assert_true(paths.PENEWORK_ROOT_PATH.endswith("penework"))
        assert_true(paths.PENEWORK_OUTPUT_PATH.endswith("output"))
