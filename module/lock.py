import os
import fcntl
import mavc.info as info
import mavc.interface as interface

# Implementation of the lock system
# Stored as files
# A lock file is just an integer
class FileLock(interface.BaseLock):
    def __init__(self):
        pass

    def Lock(self, identifier):
        if not isinstance(identifier, str) or not info.IsDirFile(identifier):
            info.Log.InternalError('Bad identifier')

        try:
            with open(info.LockDir + identifier, 'wb+') as File:
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
            with open(info.LockDir + identifier, 'rb+') as File:
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
