'''The implementation of the database system'''

import os
import fcntl
import cPickle as pickle
import zlib
import hashlib
from mavc import info
from mavc import interface


class FileDB(interface.BaseDB):
    '''Database based on local files
    Work under current dir
    Override methods to implement'''

    def _StrHash(self, data):
        '''Calculate the hash value'''

        pass

    def _ObjToStr(self, data):
        '''Transform an object to a string'''

        pass

    def _StrToObj(self, data):
        '''Transform a string to an object'''

        pass

    def _Compress(self, data):
        '''Compress the string'''

        pass

    def _Decompress(self, data):
        '''Decompress the string'''

        pass

    def Push(self, data, doaction, target):
        # Checking
        if not isinstance(data, interface.BaseDataType):
            info.Log.InternalError('Bad data that can not push')

        # Pre processing
        if doaction:
            data.OnPush(target)

        info.Log.Message('Generating datastream')

        StrMemData = self._ObjToStr(data)
        StrHash = self._StrHash(StrMemData)
        if info.DoCompress:
            StrFileData = self._Compress(StrMemData)
        else:
            StrFileData = StrMemData

        Identifier = StrHash
        TempIdentifier = info.IDTemp + StrHash

        info.Log.Message('Push data ' + Identifier)

        # Check the real file and write
        if os.path.isfile(os.path.join(info.StoreDir, Identifier)):
            # Check if the data is the same
            try:
                with open(
                    os.path.join(info.StoreDir, Identifier), 'rb'
                ) as File:
                    fcntl.flock(File, fcntl.LOCK_EX)
                    if File.read() == StrFileData:
                        info.Log.Message(
                            'Database file already exist ' + Identifier
                        )
                    else:
                        info.Log.Error(
                            'Hash conflict or bad database file ' + Identifier
                        )
            except:
                info.Log.Error('Can not open database file ' + Identifier)
        else:
            # Write to temporary file
            try:
                with open(
                    os.path.join(info.StoreDir, TempIdentifier), 'wb'
                ) as File:
                    fcntl.flock(File, fcntl.LOCK_EX)
                    File.write(StrFileData)
            except:
                info.Log.Error(
                    'Can not write temporary file ' + TempIdentifier
                )

            # Apply from temporary file
            try:
                os.rename(
                    os.path.join(info.StoreDir, TempIdentifier),
                    os.path.join(info.StoreDir, Identifier)
                )
                info.Log.Message('Database file written ' + Identifier)
                if doaction:
                    info.Log.Progress('Database stored ' + Identifier)
            except:
                info.Log.Error('Can not write database file ' + Identifier)

        return Identifier

    def Pull(self, identifier, doaction, target):
        # Checking
        if not isinstance(identifier, str) or not info.IsDirFile(identifier):
            info.Log.InternalError('Bad identifier')

        # Read from file
        if not os.path.isfile(os.path.join(info.StoreDir, identifier)):
            info.Log.Error('Database file not exist ' + identifier)

        info.Log.Message('Pull data ' + identifier)

        try:
            with open(os.path.join(info.StoreDir, identifier), 'rb') as File:
                fcntl.flock(File, fcntl.LOCK_EX)
                StrFileData = File.read()
        except:
            info.Log.Error('Can not open database file ' + identifier)

        # Finishing processing
        info.Log.Message('Restoring data')

        if info.DoCompress:
            StrMemData = self._Decompress(StrFileData)
        else:
            StrMemData = StrFileData

        StrHash = self._StrHash(StrMemData)
        if not StrHash in identifier:
            info.Log.Error('Bad database file ' + identifier)

        Obj = self._StrToObj(StrMemData)

        if isinstance(Obj, interface.BaseDataType):
            if info.Compatible(Obj.DataVer):
                info.Log.Message('Database file read ' + identifier)
                if doaction:
                    Obj.OnPull(target)
                    info.Log.Progress('Data restored ' + identifier)
                return Obj
            else:
                info.Log.InternalError('Version not supported ' + identifier)
        else:
            info.Log.InternalError('Bad data from the database ' + identifier)

    def PullLocked(self):
        return {self.Pull(item, False, None) for item in info.Lock.AllLocked()}

    def GarbageCollection(self):
        info.Log.Message('Generating garbage list')

        # Assumed everything to be garbage at first
        try:
            Garbage = set(os.listdir(info.StoreDir))
        except:
            info.Log.Error('Can not list database dir')

        def NotGarbage(item):
            '''Remove items from the garbage list'''

            if item in Garbage:
                Garbage.remove(item)
                Ref = self.Pull(item, False, None).Ref()
                for refitem in Ref:
                    NotGarbage(refitem)

        for item in info.Lock.AllLocked():
            NotGarbage(item)

        info.Log.Hint('Total garbage ' + str(len(Garbage)))
        info.Log.Message('Move garbage to ' + info.GarbageDir)

        for garbageitem in Garbage:
            info.Log.Progress('Found garbage ' + garbageitem)
            try:
                os.rename(
                    os.path.join(info.StoreDir, garbageitem),
                    os.path.join(info.GarbageDir, garbageitem)
                )
                info.Log.Message('Garbage moved ' + garbageitem)
            except:
                info.Log.Error('Can not move ' + garbageitem)

        info.Log.Progress('GC finished')


class PickleZlibDB(FileDB):
    '''Implementation of the database system
    Use zlib to hash and compress data
    Use cPickle to store objects'''

    # No longer abstract
    def __init__(self):
        pass

    # Calculate hash value, return result as string
    def _StrHash(self, data):
        try:
            ver = data.DataVer
            data.DataVer = None

            if info.StrongHash:
                # Hex value of SHA-1 checksum
                return hashlib.sha1(data).hexdigest()
            else:
                # Hex value of Adler-32 checksum
                return hex(zlib.adler32(data) & 0xffffffff)

            data.DataVer = ver
        except:
            info.Log.InternalError('Zlib Adler-32 Hash failed')

    def _ObjToStr(self, data):
        try:
            return pickle.dumps(data, info.BinaryStore)
        except:
            info.Log.InternalError('Pickle can not dump data')

    def _StrToObj(self, data):
        try:
            return pickle.loads(data)
        except:
            info.Log.InternalError('Pickle can not load data')

    def _Compress(self, data):
        try:
            return zlib.compress(data, info.CompressLevel)
        except:
            info.Log.InternalError('Zlib can not compress data')

    def _Decompress(self, data):
        try:
            return zlib.decompress(data)
        except:
            info.Log.InternalError('Zlib can not decompress data')
