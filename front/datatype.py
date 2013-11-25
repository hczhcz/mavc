from mavc import info
from mavc import datatype

def Package(comment, *data):
    '''Create package data object'''

    info.LastData = datatype.PackageDataType(comment, set(data))
    return info.LastData

def Commit(comment, *data):
    '''Create commit data object'''

    info.LastData = datatype.CommitDataType(comment, set(data))
    return info.LastData

def CommitWithTime(comment, time, *data):
    '''Create commit data object and set time stamp manually'''

    info.LastData = datatype.CommitDataType(comment, set(data), time)
    return info.LastData

def Task(comment, *data):
    '''Create task data object'''

    info.LastData = datatype.TaskDataType(comment, list(data))
    return info.LastData

def Dir(targetdir, *data):
    '''Create dir data object'''

    info.LastData = datatype.DirDataType(targetdir, set(data))
    return info.LastData

def File(targetfile):
    '''Create file data object'''

    info.LastData = datatype.FileDataType(targetfile)
    return info.LastData
