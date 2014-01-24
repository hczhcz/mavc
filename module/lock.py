'''The implementation of the lock system'''

import os
import fcntl
from mavc import info
from mavc import interface


class FileLock(interface.BaseLock):
    '''Implementation of the lock system
    Stored as files
    A lock file is just an integer'''

    def __init__(self):
        pass

    def Lock(self, identifier):
        if not isinstance(identifier, str) or not info.IsDirFile(identifier):
            info.Log.InternalError('Bad identifier')

        try:
            Path = os.path.join(info.LockDir, identifier)
            OpenCmd = 'rb+' if os.path.exists(Path) else 'wb+'

            with open(Path, OpenCmd) as File:
                fcntl.flock(File, fcntl.LOCK_EX)

                LockData = File.read()

                if LockData == '':
                    LockCount = 1
                else:
                    LockCount = int(LockData) + 1

                if LockCount < 1:
                    info.Log.Error('Bad lock on locking ' + identifier)

                LockData = str(LockCount)
                File.truncate()
                File.seek(0)
                File.write(LockData)

            info.Log.Progress('Locked ' + identifier + ' to ' + LockData)
        except:
            info.Log.Error('Can not lock ' + identifier)

    def Unlock(self, identifier):
        if not isinstance(identifier, str) or not info.IsDirFile(identifier):
            info.Log.InternalError('Bad identifier')

        try:
            with open(os.path.join(info.LockDir, identifier), 'rb+') as File:
                fcntl.flock(File, fcntl.LOCK_EX)

                LockData = File.read()

                LockCount = int(LockData) - 1

                if LockCount < 0:
                    info.Log.Error('Bad lock on unlocking ' + identifier)

                LockData = str(LockCount)
                File.truncate()
                File.seek(0)
                File.write(LockData)

            info.Log.Progress('Unlocked ' + identifier + ' to ' + LockData)
        except:
            info.Log.Error('Can not unlock ' + identifier)

    def AllLocked(self):
        try:
            return set(os.listdir(info.LockDir))
        except:
            info.Log.Error('Can not list lock dir')
