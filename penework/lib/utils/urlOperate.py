#!/usr/bin/env python
# encoding: utf-8
# encoding: utf-8
# encoding: utf-8

import urlparse
import re
import os
import sys
from urllib import unquote

from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING

def hashUrl(url):

    urlParse = urlparse.urlparse(url)
    urlSchemePath = urlparse.urljoin(urlParse.scheme, urlParse.netloc + urlParse.path)
    urlQueryKeys = (urlparse.parse_qs(urlParse.query)).keys()
    # combine urlSchemaPath and urlQueryKeys as urlHashData
    urlQueryKeys.append(urlSchemePath)
    urlQueryKeys.sort()
    hashData = hash(str(urlQueryKeys))

    return hashData


def urlDecode(url):
    url = url.strip()
    try:
        url = str(url)
    except Exception, ex:
        logger.log(CUSTOM_LOGGING.ERROR, ex)
        try:
            url = url.encode('utf-8')
        except Exception, ex:
            logger.log(CUSTOM_LOGGING.ERROR, ex)
    while re.search('%\w{2}', url):
        url = unquote(url)
    return url

