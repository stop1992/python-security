#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 penework developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

from penework.lib.core.common import getFileItems
from penework.lib.core.data import paths


def getWeakPassword():
    return getFileItems(paths.WEAK_PASS)


def getLargeWeakPassword():
    return getFileItems(paths.LARGE_WEAK_PASS)
