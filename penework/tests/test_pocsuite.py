#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 penework developers (http://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

from penework import penework_cli
from penework import penework_verify
from penework import penework_attack
from penework import penework_console

from penework.penework_cli import modulePath
from penework.lib.core.common import setPaths
from penework.lib.core.data import paths

from nose.tools import assert_true


class TestPocsuiteBase(object):

    def test_penework_setpath(self):
        paths.POCSUITE_ROOT_PATH = modulePath()
        setPaths()
        assert_true(paths.POCSUITE_ROOT_PATH.endswith("penework"))
        assert_true(paths.POCSUITE_OUTPUT_PATH.endswith("output"))
