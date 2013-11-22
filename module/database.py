import os
import fcntl
import cPickle as pickle
import zlib
import mavc.info as info
import mavc.interface as interface

# Database based on local files
# Work under current dir
# Override methods to implement
class FileDB(interface.BaseDB):
    def _StrHash(self, data):
        pass

    def _ObjToStr(self, data):
        pass

    def _StrToObj(self, data):
        pass

    def _Compress(self, data):
        pass

    def _Decompress(self, data):
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
        if os.path.isfile(info.StoreDir + Identifier):
            # Check if the data is the same
            try:
                with open(info.StoreDir + Identifier, 'rb') as File:
                    fcntl.flock(File, fcntl.LOCK_EX)
                    if File.read() == StrFileData:
                        info.Log.Message('Database file already exist '
                            + Identifier)
                    else:
                        info.Log.Error('Hash conflict or bad database file '
                            + Identifier)
            except:
                info.Log.Error('Can not open database file ' + Identifier)
        else:
            # Write to temporary file
            try:
                with open(info.StoreDir + TempIdentifier, 'wb') as File:
                    fcntl.flock(File, fcntl.LOCK_EX)
                    File.write(StrFileData)
            except:
                info.Log.Error('Can not write temporary file ' + TempIdentifier)

            # Apply from temporary file
            try:
                os.rename(info.StoreDir + TempIdentifier,
                    info.StoreDir + Identifier)
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
        if not os.path.isfile(info.StoreDir + identifier):
            info.Log.Error('Database file not exist ' + identifier)

        info.Log.Message('Pull data ' + identifier)

        try:
            with open(info.StoreDir + identifier, 'rb') as File:
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

    def Defrag(self):
        info.Log.Message('Generating frag list')

        # Assumed everything to be frag at first
        try:
            Frag = set(os.listdir(info.StoreDir))
        except:
            info.Log.Error('Can not list database dir')

        # Remove from frag list
        def NotFrag(item):
            if item in Frag:
                Frag.remove(item)
                Ref = self.Pull(item, False, None).Ref()
                for refitem in Ref:
                    NotFrag(refitem)

        for item in info.Lock.AllLocked():
            NotFrag(item)

        info.Log.Hint('Total frag ' + str(len(Frag)))
        info.Log.Message('Move frag to ' + info.FragDir)

        for fragitem in Frag:
            info.Log.Progress('Found frag ' + fragitem)
            try:
                os.rename(info.StoreDir + fragitem, info.FragDir + fragitem)
                info.Log.Message('Frag moved ' + fragitem)
            except:
                info.Log.Error('Can not defrag ' + fragitem)

        info.Log.Progress('Defragment finished')

# Implementation of the database system
# Use zlib to hash and compress data
# Use cPickle to store objects
class PickleZlibDB(FileDB):
    # No longer abstract
    def __init__(self):
        pass

    # Return a string like 0x12345678
    def _StrHash(self, data):
        try:
            # Hex value of Adler-32 checksum
            return hex(zlib.adler32(data) & 0xffffffff)
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
