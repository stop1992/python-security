#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 penework developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""


class PeneworkBaseException(Exception):
    pass


class PeneworkUserQuitException(PeneworkBaseException):
    pass


class PeneworkDataException(PeneworkBaseException):
    pass


class PeneworkGenericException(PeneworkBaseException):
    pass


class PeneworkSystemException(PeneworkBaseException):
    pass


class PeneworkFilePathException(PeneworkBaseException):
    pass


class PeneworkConnectionException(PeneworkBaseException):
    pass


class PeneworkThreadException(PeneworkBaseException):
    pass


class PeneworkValueException(PeneworkBaseException):
    pass


class PeneworkMissingPrivileges(PeneworkBaseException):
    pass


class PeneworkSyntaxException(PeneworkBaseException):
    pass
