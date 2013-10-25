import os
import mavc.info as info
import mavc.interface as interface

# Implementation of the lock system
# Stored as files
# A lock file is just an integer
class FileLock(interface.BaseLock):
    def __init__(self):
        pass

    def Lock(self, id):
        LockCount = 1

        try:
            if os.path.isfile(info.LockDir + id):
                with open(info.LockDir + id, 'rb') as File:
                    LockData = File.read()
                LockCount = int(LockData) + 1

            LockData = str(LockCount)

            if LockCount >= 1:
                with open(info.LockDir + id, 'wb') as File:
                    File.write(LockData)
                info.Log.Progress('Locked ' + id + ' to ' + LockData)
        except:
            info.Log.Error('Can not lock ' + id)

        if LockCount < 1:
            info.Log.Error('Bad lock on locking ' + id)

    def Unlock(self, id):
        LockCount = -1

        try:
            if os.path.isfile(info.LockDir + id):
                with open(info.LockDir + id, 'rb') as File:
                    LockData = File.read()
                LockCount = int(LockData) - 1

            LockData = str(LockCount)

            if LockCount >= 1:
                with open(info.LockDir + id, 'wb') as File:
                    File.write(LockData)
                info.Log.Progress('Unlocked ' + id + ' to ' + LockData)
        except:
            info.Log.Error('Can not unlock ' + id)

        if LockCount < 0:
            info.Log.Error('Bad lock on unlocking ' + id)

        if LockCount == 0:
            try:
                os.remove(info.LockDir + id)
                info.Log.Progress('Fully unlocked ' + id)
            except:
                info.Log.Error('Can not fully unlock ' + id)

    def AllLocked(self):
        try:
            return set(os.listdir(info.LockDir))
        except:
            info.Log.Error('Can not list lock dir')
