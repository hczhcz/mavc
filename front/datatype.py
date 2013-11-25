from mavc import datatype

def Package(comment, *data):
    return datatype.PackageDataType(comment, set(data))

def Commit(comment, *data):
    return datatype.CommitDataType(comment, set(data))

def CommitWithTime(comment, time, *data):
    return datatype.CommitDataType(comment, set(data), time)

def Task(comment, *data):
    return datatype.TaskDataType(comment, list(data))

def Dir(targetdir, *data):
    return datatype.DirDataType(targetdir, set(data))

def File(targetfile):
    return datatype.FileDataType(targetfile)
