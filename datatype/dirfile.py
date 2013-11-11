import os
import fcntl
import mavc.info as info
from abstract import *

class DirDataType(DirFileDataType, SetDataType):
    def __init__(self, dir, data):
        info.Log.Progress('Dir ' + dir)
        self._SetTarget(dir)
        self._SetData(data)

    def _DoOnPush(self):
        OldDir = info.WorkingDir
        NewDir = OldDir + self._Target + os.sep

        # Check dir
        if os.path.exists(NewDir):
            info.Log.Message('Dir checked ' + NewDir)
        else:
            info.Log.Error('Dir not exist ' + NewDir)

        # With new dir do push
        try:
            info.WorkingDir = OldDir + self._Target + os.sep
            super(DirDataType, self)._DoOnPush()
        except:
            raise
        finally:
            info.WorkingDir = OldDir

    def _DoOnPull(self):
        OldDir = info.WorkingDir
        NewDir = OldDir + self._Target + os.sep

        # Make dir if necessary
        if os.path.exists(NewDir):
            info.Log.Message('Dir already exist ' + NewDir)
        else:
            try:
                os.mkdir(NewDir)
                info.Log.Progress('Dir created ' + NewDir)
            except:
                info.Log.Error('Can not create dir ' + NewDir)

        # With new dir do pull
        try:
            info.WorkingDir = NewDir
            super(DirDataType, self)._DoOnPull()
        except:
            raise
        finally:
            info.WorkingDir = OldDir

class FileDataType(DirFileDataType):
    _FileData = None

    def __init__(self, file):
        info.Log.Progress('File ' + file)
        self._SetTarget(file)

    def _DoOnPush(self):
        FromFile = info.WorkingDir + self._Target

        # Read from file
        if not os.path.isfile(FromFile):
            info.Log.Error('File not exist ' + FromFile)

        try:
            with open(FromFile, 'rb') as File:
                fcntl.flock(File, fcntl.LOCK_EX)
                self._FileData = File.read()
        except:
            info.Log.Error('Can not open file ' + FromFile)

    def _DoOnPull(self):
        ToFile = info.WorkingDir + self._Target
        OutDir = info.OutputDir + info.WorkingDir
        BakDir = info.BackupDir + info.WorkingDir

        # Check the real file
        if os.path.isfile(ToFile):
            # Check if the data is the same
            try:
                with open(ToFile, 'rb') as File:
                    fcntl.flock(File, fcntl.LOCK_EX)
                    if File.read() == self._FileData:
                        info.Log.Message('File already exist ' + ToFile)
                        NeedBak = False
                        NeedWrite = False
                    else:
                        info.Log.Hint('File changed ' + ToFile)
                        NeedBak = True
                        NeedWrite = True
            except:
                info.Log.Error('Can not open file ' + ToFile)
        else:
            NeedBak = False
            NeedWrite = True

        # Do backup
        if NeedBak:
            try:
                if not os.path.exists(BakDir):
                    os.mkdir(BakDir)
                os.rename(ToFile, info.BackupDir + ToFile)
            except:
                info.Log.Error('Can not backup file ' + ToFile)

        if NeedWrite:
            # Write to buffer file
            try:
                if not os.path.exists(OutDir):
                    os.mkdir(OutDir)
                with open(info.OutputDir + ToFile, 'wb') as File:
                    fcntl.flock(File, fcntl.LOCK_EX)
                    File.write(self._FileData)
            except:
                info.Log.Error('Can not write output buffer ' + ToFile)

            # Apply from buffer file
            try:
                os.rename(info.OutputDir + ToFile, ToFile)
                info.Log.Progress('File written ' + ToFile)
            except:
                info.Log.Error('Can not write file ' + ToFile)

    def _DoRef(self):
        return set()
