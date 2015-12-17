# encoding:utf-8

import os
try:
    import fcntl
except ImportError:
    # windows platform
    fcntl = None
    import win32con
    import win32file
    import pywintypes
    LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
    overlapped = pywintypes.OVERLAPPED()

class FileLock(object):

    # def __init__ (self, filename=None):
    def __init__ (self, fileobject_):

        # if filename:
            # self.filename = filename
            # self.handle = open(self.filename, 'w')

        if fileobject_:
            self.handle = fileobject_
        else:
            print '[*] Not exists file name'

    def acquire(self):

        if fcntl:
            fcntl.flock(self.handle, fcntl.LOCK_EX)
        else:
            hfile = win32file._get_osfhandle(self.handle.fileno())
            win32file.LockFileEx(hfile, LOCK_EX, 0, -0x10000, overlapped)

    def release(self):

        if fcntl:
            fcntl.flock(self.handle, fcntl.LOCK_UN)
        else:
            hfile = win32file._get_osfhandle(self.handle.fileno())
            win32file.UnlockFileEx(hfile, 0, -0x10000, overlapped)

    # def __del__(self):

        # try:
            # self.handle.close()
            # os.remove(self.filename)
        # except:
            # pass
