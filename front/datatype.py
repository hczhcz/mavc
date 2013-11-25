from mavc import datatype

def Package(comment, *data):
    '''Create package data object'''

    return datatype.PackageDataType(comment, set(data))

def Commit(comment, *data):
    '''Create commit data object'''

    return datatype.CommitDataType(comment, set(data))

def CommitWithTime(comment, time, *data):
    '''Create commit data object and set time stamp manually'''

    return datatype.CommitDataType(comment, set(data), time)

def Task(comment, *data):
    '''Create task data object'''

    return datatype.TaskDataType(comment, list(data))

def Dir(targetdir, *data):
    '''Create dir data object'''

    return datatype.DirDataType(targetdir, set(data))

def File(targetfile):
    '''Create file data object'''

    return datatype.FileDataType(targetfile)
