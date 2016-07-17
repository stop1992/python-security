#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 penework developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import time
import socket
from lib.core.data import kb
from lib.core.data import conf
from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING
from lib.core.common import filepathParser
from lib.core.common import multipleReplace
from lib.core.common import StringImporter
from lib.core.common import delModule
from lib.core.settings import POC_IMPORTDICT
from lib.core.settings import HTTP_DEFAULT_HEADER


class Cannon():

    def __init__(self, target, info={}, mode='veirfy', params={}, headers={}, timeout=30):
        self.target = target
        self.pocString = info["pocstring"]
        self.pocName = info["pocname"].replace('.', '')
        self.mode = mode if mode in ('verify', 'attack') else 'verify'
        self.delmodule = False
        self.params = params
        conf.isPycFile = info.get('ispycfile', False)
        conf.httpHeaders = HTTP_DEFAULT_HEADER
        if headers:
            conf.httpHeaders.update(headers)

        try:
            kb.registeredPocs
        except Exception:
            kb.registeredPocs = {}

        self.registerPoc()
        self._setHTTPTimeout(timeout)

    def _setHTTPTimeout(self, timeout):
        """
        Set the HTTP timeout
        """
        timeout = float(timeout)
        socket.setdefaulttimeout(timeout)

    def registerPoc(self):
        pocString = multipleReplace(self.pocString, POC_IMPORTDICT)
        _, self.moduleName = filepathParser(self.pocName)
        try:
            importer = StringImporter(self.moduleName, pocString)
            importer.load_module(self.moduleName)
        except ImportError, ex:
            logger.log(CUSTOM_LOGGING.ERROR, ex)

    def run(self):
        try:
            poc = kb.registeredPocs[self.moduleName]
            result = poc.execute(self.target, headers=conf.httpHeaders, mode=self.mode, params=self.params)
            output = (self.target, self.pocName, result.vulID, result.appName, result.appVersion, (1, "success") if result.is_success() else result.error, time.strftime("%Y-%m-%d %X", time.localtime()), str(result.result))

            if self.delmodule:
                delModule(self.moduleName)
            return output
        except Exception, ex:
            logger.log(CUSTOM_LOGGING.ERROR, ex)
