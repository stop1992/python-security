#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 penework developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

from penework.lib.core.data import logger
from penework.lib.core.enums import CUSTOM_LOGGING

from penework.lib.utils.password import getLargeWeakPassword
from penework.lib.utils.password import getWeakPassword

from penework.lib.utils.funs import url2ip
from penework.lib.utils.funs import getExtPar
from penework.lib.utils.funs import strToDict
from penework.lib.utils.funs import randomStr

from penework.lib.utils.funs import writeText
from penework.lib.utils.funs import writeBinary
from penework.lib.utils.funs import loadText
from penework.lib.utils.funs import resolve_js_redirects
