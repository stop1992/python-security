#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 penework developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING

from lib.utils.password import getLargeWeakPassword
from lib.utils.password import getWeakPassword

from lib.utils.funs import url2ip
from lib.utils.funs import getExtPar
from lib.utils.funs import strToDict
from lib.utils.funs import randomStr

from lib.utils.funs import writeText
from lib.utils.funs import writeBinary
from lib.utils.funs import loadText
from lib.utils.funs import resolve_js_redirects
