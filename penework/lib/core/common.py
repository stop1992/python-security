#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 penework developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import os
import re
import sys
import imp
import ntpath
import locale
import inspect
import posixpath
import marshal
import unicodedata
import urlparse
from StringIO import StringIO
from lib.core.convert import base64pickle
from lib.core.convert import base64unpickle
from lib.core.convert import hexdecode
from lib.core.convert import htmlunescape
from lib.core.convert import stdoutencode
from lib.core.convert import unicodeencode
from lib.core.convert import utf8encode
from lib.core.data import conf
from lib.core.convert import stdoutencode
from lib.core.log import LOGGER_HANDLER
from lib.core.enums import CUSTOM_LOGGING
from lib.core.enums import HTTPMETHOD
from lib.core.data import paths
from lib.core.data import kb
from lib.core.data import logger
from lib.core.data import paths
# from lib.core.data import formData
from lib.core.exception import PeneworkGenericException
from thirdparty.odict.odict import OrderedDict
from lib.core.settings import (BANNER, GIT_PAGE, ISSUES_PAGE, PLATFORM, PYVERSION, VERSION_STRING)
from lib.core.settings import FORM_SEARCH_REGEX
from lib.core.settings import UNICODE_ENCODING, INVALID_UNICODE_CHAR_FORMAT
from lib.core.exception import PeneworkSystemException
from thirdparty.termcolor.termcolor import colored
from thirdparty.clientform.clientform import ParseResponse
from thirdparty.clientform.clientform import ParseError


class StringImporter(object):

    """
    Use custom meta hook to import modules available as strings.
    Cp. PEP 302 http://www.python.org/dev/peps/pep-0302/#specification-part-2-registering-hooks
    """

    def __init__(self, fullname, contents):
        self.fullname = fullname
        self.contents = contents

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]

        mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
        mod.__file__ = "<%s>" % fullname
        mod.__loader__ = self
        if conf.isPycFile:
            code = marshal.loads(self.contents[8:])
        else:
            code = compile(self.contents, mod.__file__, "exec")
        exec code in mod.__dict__
        return mod


def delModule(modname, paranoid=None):
    from sys import modules
    try:
        thismod = modules[modname]
    except KeyError:
        raise ValueError(modname)
    these_symbols = dir(thismod)
    if paranoid:
        try:
            paranoid[:]  # sequence support
        except:
            raise ValueError('must supply a finite list for paranoid')
        else:
            these_symbols = paranoid[:]
    del modules[modname]
    for mod in modules.values():
        try:
            delattr(mod, modname)
        except AttributeError:
            pass
        if paranoid:
            for symbol in these_symbols:
                if symbol[:2] == '__':  # ignore special symbols
                    continue
                try:
                    delattr(mod, symbol)
                except AttributeError:
                    pass


def banner():
    """
    Function prints penework banner with its version
    """
    _ = BANNER
    if not getattr(LOGGER_HANDLER, "is_tty", False):
        _ = re.sub("\033.+?m", "", _)
    dataToStdout(_)


def dataToStdout(data, bold=False):
    """
    Writes text to the stdout (console) stream
    """
    if 'quiet' not in conf or not conf.quiet:
        message = ""

        if isinstance(data, unicode):
            message = stdoutencode(data)
        else:
            message = data

        sys.stdout.write(setColor(message, bold))

        try:
            sys.stdout.flush()
        except IOError:
            pass
    return


def setColor(message, bold=False):
    retVal = message

    if message and getattr(LOGGER_HANDLER, "is_tty", False):  # colorizing handler
        if bold:
            retVal = colored(message, color=None, on_color=None, attrs=("bold",))

    return retVal


def unhandledExceptionMessage():
    """
    Returns detailed message about occurred unhandled exception
    """

    errMsg = "unhandled exception occurred in %s. It is recommended to retry your " % VERSION_STRING
    errMsg += "run with the latest development version from official Gitlab "
    errMsg += "repository at '%s'. If the exception persists, please open a new issue " % GIT_PAGE
    errMsg += "at '%s' " % ISSUES_PAGE
    errMsg += "with the following text and any other information required to "
    errMsg += "reproduce the bug. The "
    errMsg += "developers will try to reproduce the bug, fix it accordingly "
    errMsg += "and get back to you\n"
    errMsg += "penework version: %s\n" % VERSION_STRING[VERSION_STRING.find('/') + 1:]
    errMsg += "Python version: %s\n" % PYVERSION
    errMsg += "Operating system: %s\n" % PLATFORM
    errMsg += "Command line: %s\n" % re.sub(r".+?\bpy\b", "py", " ".join(sys.argv))

    return errMsg


def filepathParser(path):
    return ntpath.split(ntpath.splitext(path)[0])


def changeToPyImportType(path):
    """
    >>> changeToPyImportType('/path/to/module.py')
    'path.to.module'
    >>> changeToPyImportType('path/to/module.py')
    'path.to.module'
    >>> changeToPyImportType('path/to')
    'path.to'
    """

    return ntpath.splitext(path)[0].strip("/").replace("/", ".")


def multipleReplace(text, adict):
    rx = re.compile("|".join(map(re.escape, adict)))

    def oneXlat(match):
        return adict[match.group(0)]
    return rx.sub(oneXlat, text)


def getUnicode(value, encoding=None, noneToNull=False):
    """
    Return the unicode representation of the supplied value:

    >>> getUnicode(u'test')
    u'test'
    >>> getUnicode('test')
    u'test'
    >>> getUnicode(1)
    u'1'
    """

    if noneToNull and value is None:
        return u'NULL'

    if isListLike(value):
        value = list(getUnicode(_, encoding, noneToNull) for _ in value)
        return value

    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):
        while True:
            try:
                return unicode(value, encoding or UNICODE_ENCODING)
            except UnicodeDecodeError, ex:
                try:
                    return unicode(value, UNICODE_ENCODING)
                except:
                    value = value[:ex.start] + "".join(INVALID_UNICODE_CHAR_FORMAT % ord(_) for _ in value[ex.start:ex.end]) + value[ex.end:]
    else:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            return unicode(str(value), errors="ignore")  # encoding ignored for non-basestring instances


def isListLike(value):
    """
    Returns True if the given value is a list-like instance

    >>> isListLike([1, 2, 3])
    True
    >>> isListLike(u'2')
    False
    """

    return isinstance(value, (list, tuple, set))


def readFile(filename):
    try:
        with open(filename) as f:
            retVal = f.read()
    except IOError, ex:
        errMsg = "something went wrong while trying to read "
        errMsg += "the input file ('%s')" % ex
        raise PeneworkGenericException(errMsg)
    return retVal


def writeFile(filename, data):
    try:
        with open(filename, "w") as f:
            f.write(data)
    except IOError, ex:
        errMsg = "something went wrong while trying to write "
        errMsg += "to the output file ('%s')" % ex
        raise PeneworkGenericException(errMsg)


def setPaths():
    """
    Sets absolute paths for project directories and files
    """

    paths.PENEWORK_LIB_PATH = os.path.join(paths.PENEWORK_ROOT_PATH, "lib")
    paths.PENEWORK_DATA_PATH = os.path.join(paths.PENEWORK_ROOT_PATH, "data")
    paths.PENEWORK_PLUGINS_PATH = os.path.join(paths.PENEWORK_ROOT_PATH, "plugins")
    paths.PENEWORK_API_PATH = os.path.join(paths.PENEWORK_ROOT_PATH, "api")
    paths.PENEWORK_EXPLOIT_PATH = os.path.join(paths.PENEWORK_ROOT_PATH, "exploit")
    paths.PENEWORK_THIRDPARTY_PATH = os.path.join(paths.PENEWORK_ROOT_PATH, "thirdparty")

    paths.USER_AGENTS = os.path.join(paths.PENEWORK_DATA_PATH, "user-agents.txt")
    paths.WEAK_PASS = os.path.join(paths.PENEWORK_DATA_PATH, "password-top100.txt")
    paths.LARGE_WEAK_PASS = os.path.join(paths.PENEWORK_DATA_PATH, "password-top1000.txt")

    _ = os.path.join(os.path.expanduser("~"), ".penework")
    paths.PENEWORK_OUTPUT_PATH = getUnicode(paths.get("PENEWORK_OUTPUT_PATH", os.path.join(_, "output")), encoding=sys.getfilesystemencoding())

    paths.PENEWORK_MODULES_PATH = os.path.join(_, "modules")
    paths.PENEWORK_TMP_PATH = os.path.join(paths.PENEWORK_MODULES_PATH, "tmp")
    paths.PENEWORK_HOME_PATH = os.path.expanduser("~")
    paths.PENEWORK_RC_PATH = paths.PENEWORK_HOME_PATH + "/.peneworkrc"


def getFileItems(filename, commentPrefix='#', unicode_=True, lowercase=False, unique=False):
    """
    @function returns newline delimited items contained inside file
    """

    retVal = list() if not unique else OrderedDict()

    checkFile(filename)

    try:
        with open(filename, 'r') as f:
            for line in (f.readlines() if unicode_ else f.xreadlines()):
                # xreadlines doesn't return unicode strings when codecs.open() is used
                if commentPrefix and line.find(commentPrefix) != -1:
                    line = line[:line.find(commentPrefix)]

                line = line.strip()

                if not unicode_:
                    try:
                        line = str.encode(line)
                    except UnicodeDecodeError:
                        continue

                if line:
                    if lowercase:
                        line = line.lower()

                    if unique and line in retVal:
                        continue

                    if unique:
                        retVal[line] = True

                    else:
                        retVal.append(line)

    except (IOError, OSError, MemoryError), ex:
        errMsg = "something went wrong while trying "
        errMsg += "to read the content of file '%s' ('%s')" % (filename, ex)
        raise PeneworkSystemException(errMsg)

    return retVal if not unique else retVal.keys()


def checkFile(filename):
    """
    @function Checks for file existence and readability
    """

    valid = True

    if filename is None or not os.path.isfile(filename):
        valid = False

    if valid:
        try:
            with open(filename, "rb"):
                pass
        except:
            valid = False

    if not valid:
        raise PeneworkSystemException("unable to read file '%s'" % filename)


def choosePocType(filepath):
    """
    @function choose '.py' or '.json' extension to load the poc file
    """
    return ntpath.splitext(filepath)[1][1:]


def safeExpandUser(filepath):
    """
    @function Patch for a Python Issue18171 (http://bugs.python.org/issue18171)
    """

    retVal = filepath

    try:
        retVal = os.path.expanduser(filepath)
    except UnicodeDecodeError:
        _ = locale.getdefaultlocale()
        retVal = getUnicode(os.path.expanduser(filepath.encode(_[1] if _ and len(_) > 1 else UNICODE_ENCODING)))

    return retVal


def parseTargetUrl(url):
    """
    Parse target URL
    """
    retVal = url

    if not re.search("^http[s]*://", retVal, re.I) and not re.search("^ws[s]*://", retVal, re.I):
        if re.search(":443[/]*$", retVal):
            retVal = "https://" + retVal
        else:
            retVal = "http://" + retVal

    return retVal


def normalizePath(filepath):
    """
    Returns normalized string representation of a given filepath

    >>> normalizePath('//var///log/apache.log')
    '//var/log/apache.log'
    """

    retVal = filepath

    if retVal:
        retVal = retVal.strip("\r\n")
        retVal = ntpath.normpath(retVal) if isWindowsDriveLetterPath(retVal) else posixpath.normpath(retVal)

    return retVal


def isWindowsDriveLetterPath(filepath):
    """
    Returns True if given filepath starts with a Windows drive letter

    >>> isWindowsDriveLetterPath('C:\\boot.ini')
    True
    >>> isWindowsDriveLetterPath('/var/log/apache.log')
    False
    """

    return re.search("\A[\w]\:", filepath) is not None


def normalizeUnicode(value):
    """
    Does an ASCII normalization of unicode strings
    Reference: http://www.peterbe.com/plog/unicode-to-ascii

    >>> normalizeUnicode(u'\u0161u\u0107uraj')
    'sucuraj'
    """

    return unicodedata.normalize('NFKD', value).encode('ascii', 'ignore') if isinstance(value, unicode) else value


def getPublicTypeMembers(type_, onlyValues=False):
    """
    Useful for getting members from types (e.g. in enums)

    >>> [_ for _ in getPublicTypeMembers(OS, True)]
    ['Linux', 'Windows']
    """

    for name, value in inspect.getmembers(type_):
        if not name.startswith('__'):
            if not onlyValues:
                yield (name, value)
            else:
                yield value


def reIndent(s, numSpace):
    leadingSpace = numSpace * ' '
    lines = [leadingSpace + line for line in s.splitlines()]
    return '\n'.join(lines)




def findPageForms(content, url, raise_=False):
    """
    Parses given page content for possible forms
    """

    class _(StringIO):
        def __init__(self, content, url):
            StringIO.__init__(self, unicodeencode(content, kb.pageEncoding) if isinstance(content, unicode) else content)
            self._url = url
        def geturl(self):
            return self._url

    if not content:
        errMsg = "can't parse forms as the page content appears to be blank"
        if raise_:
            raise PeneworkGenericException(errMsg)
        else:
            logger.log(CUSTOM_LOGGING.SYSINFO, errMsg)

    forms = None
    retVal = set()
    response = _(content, url)

    try:
        forms = ParseResponse(response, backwards_compat=False)
    except (UnicodeError, ValueError):
        pass
    except ParseError:
        if "<html" in (content or ""):
            warnMsg = "badly formed HTML at the given URL ('%s'). Going to filter it" % url
            logger.log(CUSTOM_LOGGING.WARN, warnMsg)
            filtered = _("".join(re.findall(FORM_SEARCH_REGEX, content)), url)
            try:
                forms = ParseResponse(filtered, backwards_compat=False)
            except ParseError:
                errMsg = "no success"
                if raise_:
                    raise PeneworkGenericException(errMsg)
                else:
                    logger.log(CUSTOM_LOGGING.SYSINFO,errMsg)

    if forms:
        for form in forms:
            try:
                for control in form.controls:
                    if hasattr(control, "items") and not any((control.disabled, control.readonly)):
                        # if control has selectable items select first non-disabled
                        for item in control.items:
                            if not item.disabled:
                                if not item.selected:
                                    item.selected = True
                                break

                request = form.click()
            except (ValueError, TypeError), ex:
                errMsg = "there has been a problem while "
                errMsg += "processing page forms ('%s')" % getSafeExString(ex)
                if raise_:
                    raise PeneworkGenericException(errMsg)
                else:
                    logger.log(CUSTOM_LOGGING.SYSINFO, errMsg)
            else:
                url = request.get_full_url()
                method = request.get_method()
                data = request.get_data() if request.has_data() else None

                if not data and method and method.upper() == HTTPMETHOD.POST:
                    debugMsg = "invalid POST form with blank data detected"
                    logger.log(CUSTOM_LOGGING.SYSINFO, debugMsg)
                    continue

                # flag to know if we are dealing with the same target host
                _ = reduce(lambda x, y: x == y, map(lambda x: urlparse.urlparse(x).netloc.split(':')[0], (response.geturl(), url)))

                if conf.scope:
                    if not re.search(conf.scope, url, re.I):
                        continue
                elif not _:
                    continue
                else:
                    formData = (url, method, data, conf.cookie)
                    retVal.add(formData)
    else:
        errMsg = "there were no forms found at the given target URL"
        if raise_:
            raise PeneworkGenericException(errMsg)
        else:
            logger.log(CUSTOM_LOGGING.SYSINFO, errMsg)

    return retVal


def getUnicode(value, encoding=None, noneToNull=False):
    """
    Return the unicode representation of the supplied value:

    >>> getUnicode(u'test')
    u'test'
    >>> getUnicode('test')
    u'test'
    >>> getUnicode(1)
    u'1'
    """

    if noneToNull and value is None:
        return None

    if isListLike(value):
        value = list(getUnicode(_, encoding, noneToNull) for _ in value)
        return value

    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):
        while True:
            try:
                return unicode(value, encoding or (kb.get("pageEncoding") if kb.get("originalPage") else None) or UNICODE_ENCODING)
            except UnicodeDecodeError, ex:
                try:
                    return unicode(value, UNICODE_ENCODING)
                except:
                    value = value[:ex.start] + "".join(INVALID_UNICODE_CHAR_FORMAT % ord(_) for _ in value[ex.start:ex.end]) + value[ex.end:]
    else:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            return unicode(str(value), errors="ignore")  # encoding ignored for non-basestring instances


def getSafeExString(ex, encoding=None):
    """
    Safe way how to get the proper exception represtation as a string
    (Note: errors to be avoided: 1) "%s" % Exception(u'\u0161') and 2) "%s" % str(Exception(u'\u0161'))
    """

    retVal = ex

    if getattr(ex, "message", None):
        retVal = ex.message
    elif getattr(ex, "msg", None):
        retVal = ex.msg

    return getUnicode(retVal, encoding=encoding)
