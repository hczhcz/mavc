'''Constructors (factory) of data objects'''

from mavc import info
from mavc import datatype


def _Expand(data):
    '''If data is a list or set in another list or set, expand it'''

    if len(data) == 1 and (
        isinstance(data[0], set) or isinstance(data[0], list)
    ):
        return data[0]
    else:
        return data


def Package(comment, *data):
    '''Create package data object'''

    info.LastData = datatype.PackageDataType(comment, set(_Expand(data)))
    return info.LastData


def Commit(comment, *data):
    '''Create commit data object'''

    info.LastData = datatype.CommitDataType(comment, set(_Expand(data)))
    return info.LastData


def CommitTimed(comment, time, *data):
    '''Create commit data object and set time stamp manually'''

    info.LastData = datatype.CommitDataType(comment, set(_Expand(data)), time)
    return info.LastData


def Task(comment, *data):
    '''Create task data object'''

    info.LastData = datatype.TaskDataType(comment, list(_Expand(data)))
    return info.LastData


def Dir(targetdir, *data):
    '''Create dir data object'''

    info.LastData = datatype.DirDataType(targetdir, set(_Expand(data)))
    return info.LastData


def File(targetfile):
    '''Create file data object'''

    info.LastData = datatype.FileDataType(targetfile)
    return info.LastData
