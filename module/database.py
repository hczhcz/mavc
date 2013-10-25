import os
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

    def Push(self, data):
        # Checking
        if not isinstance(data, interface.BaseDataType):
            info.Log.InternalError('Unknown data that can not push')

        # Pre processing
        data.OnPush()

        info.Log.Message('Generating datastream')

        StrMemData = self._ObjToStr(data)
        StrHash = self._StrHash(StrMemData)
        StrFileData = self._Compress(StrMemData)\
            if info.DoCompress else StrMemData

        FileName = StrHash
        TempFileName = info.IDTemp + StrHash

        info.Log.Message('Push data ' + FileName)

        # Check the real file and write
        if os.path.isfile(info.StoreDir + FileName):
            # Check if the data is the same
            try:
                with open(info.StoreDir + FileName, 'rb') as File:
                    if File.read() == StrFileData:
                        info.Log.Message('Database file already exist '\
                            + FileName)
                    else:
                        info.Log.Error('Hash conflict or bad database file '\
                            + FileName)
            except:
                info.Log.Error('Can not open database file ' + FileName)
        else:
            # Write to temporary file
            try:
                with open(info.StoreDir + TempFileName, 'wb') as File:
                    File.write(StrFileData)
            except:
                info.Log.Error('Can not write temporary file ' + TempFileName)

            # Apply from temporary file
            try:
                os.rename(info.StoreDir + TempFileName, \
                    info.StoreDir + FileName)
                info.Log.Progress('Database file written ' + FileName)
            except:
                info.Log.Error('Can not write database file ' + FileName)

        return FileName

    def Pull(self, id, doaction = True):
        # Checking
        if not isinstance(id, str):
            info.Log.InternalError('Identifier must be string')

        # Read from file
        if not os.path.isfile(info.StoreDir + id):
            info.Log.Error('Database file not exist ' + id)

        info.Log.Message('Pull data ' + id)

        try:
            with open(info.StoreDir + id, 'rb') as File:
                StrFileData = File.read()
        except:
            info.Log.Error('Can not open database file ' + id)

        # Finishing processing
        info.Log.Message('Restoring data')
        StrMemData = self._Decompress(StrFileData)\
            if info.DoCompress else StrFileData
        StrHash = self._StrHash(StrMemData)
        if not StrHash in id:
            info.Log.Error('Bad database file ' + id)

        Obj = self._StrToObj(StrMemData)

        if isinstance(Obj, interface.BaseDataType)\
            and info.Compatible(Obj.DataVer):
            if doaction:
                Obj.OnPull()
                info.Log.Progress('Data restored ' + id)
            else:
                info.Log.Message('Database file read ' + id)
            return Obj
        else:
            info.Log.InternalError('Unknown data from the database ' + id)

    def PullLocked(self):
        return {self.Pull(item, False) for item in info.Lock.AllLocked()}

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
                Ref = self.Pull(item, False).Ref()
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
