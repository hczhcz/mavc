'''Dir and file data, data object with IO'''

import os
import fcntl
from mavc import info
import abstract


class DirDataType(abstract.DirFileDataType, abstract.SetDataType):
    '''Dir data
    Check dir on push
    Ensure dir (create if not exist) on pull'''

    def __init__(self, targetdir, data):
        self._SetTarget(targetdir)
        self._SetData(data)
        info.Log.Progress(self.AsStr())

    def AsStr(self):
        return 'Dir ' + self._Target

    def AsCode(self):
        return 'DirDataType(' + self._Target + ', ' + repr(self._Data) + ')'

    def _DoOnPush(self, target):
        self._CheckPath()

        OldDir = target
        NewDir = os.path.join(OldDir, self.Target())

        # Check dir
        if os.path.isdir(NewDir):
            info.Log.Message('Dir checked ' + NewDir)
        else:
            info.Log.Error('Dir not exist ' + NewDir)

        # With new dir do push
        super(DirDataType, self)._DoOnPush(NewDir)

    def _DoOnPull(self, target):
        self._CheckPath()

        OldDir = target
        NewDir = os.path.join(OldDir, self.Target())

        # Make dir if necessary
        if os.path.isdir(NewDir):
            info.Log.Message('Dir already exist ' + NewDir)
        else:
            try:
                os.mkdir(NewDir)
                info.Log.Progress('Dir created ' + NewDir)
            except:
                info.Log.Error('Can not create dir ' + NewDir)

        # With new dir do pull
        super(DirDataType, self)._DoOnPull(NewDir)


class FileDataType(abstract.DirFileDataType):
    '''File data
    Read file on push
    Write file on pull'''

    _FileData = None

    def __init__(self, targetfile):
        self._SetTarget(targetfile)
        info.Log.Progress(self.AsStr())

    def AsStr(self):
        return 'File ' + self._Target

    def AsCode(self):
        return 'FileDataType(' + self._Target + ')'

    def _DoOnPush(self, target):
        self._CheckPath()

        FromFile = os.path.join(target, self.Target())

        # Read from file
        if not os.path.isfile(FromFile):
            info.Log.Error('File not exist ' + FromFile)

        try:
            with open(FromFile, 'rb') as File:
                fcntl.flock(File, fcntl.LOCK_EX)
                self._FileData = File.read()
        except:
            info.Log.Error('Can not open file ' + FromFile)

    def _DoOnPull(self, target):
        self._CheckPath()

        ToFile = os.path.join(target, self.Target())
        OutDir = os.path.join(info.OutputDir, target)
        BakDir = os.path.join(info.BackupDir, target)

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
                if not os.path.isdir(BakDir):
                    os.mkdir(BakDir)
                os.rename(ToFile, os.path.join(info.BackupDir, ToFile))
            except:
                info.Log.Error('Can not backup file ' + ToFile)

        if NeedWrite:
            # Write to buffer file
            try:
                if not os.path.isdir(OutDir):
                    os.mkdir(OutDir)
                with open(os.path.join(info.OutputDir, ToFile), 'wb') as File:
                    fcntl.flock(File, fcntl.LOCK_EX)
                    File.write(self._FileData)
            except:
                info.Log.Error('Can not write output buffer ' + ToFile)

            # Apply from buffer file
            try:
                os.rename(os.path.join(info.OutputDir, ToFile), ToFile)
                info.Log.Progress('File written ' + ToFile)
            except:
                info.Log.Error('Can not write file ' + ToFile)

    def _DoRef(self):
        return set()
