'''Constructors (factory) of data objects'''

from mavc import info
from mavc import datatype


def _Expand(data):
    '''If data is a list or set in another list or set, expand it'''

    if len(data) == 0:
        data = [info.LastData]

    if len(data) == 1 and (
        isinstance(data[0], set) or isinstance(data[0], list)
    ):
        return data[0]
    else:
        return data


def Package(comment, *data):
    '''Package(comment[, data1, data2, ...])
    Create package data object'''

    info.LastData = datatype.PackageDataType(comment, set(_Expand(data)))
    return info.LastData


def Commit(comment, *data):
    '''Commit(comment[, data1, data2, ...])
    Create commit data object'''

    info.LastData = datatype.CommitDataType(comment, set(_Expand(data)))
    return info.LastData


def CommitTimed(comment, time, *data):
    '''CommitTimed(comment, time: str[, data1, data2, ...])
    Create commit data object and set time stamp manually'''

    info.LastData = datatype.CommitDataType(comment, set(_Expand(data)), time)
    return info.LastData


def Task(comment, *data):
    '''Task(comment[, data1, data2, ...])
    Create task data object'''

    info.LastData = datatype.TaskDataType(comment, list(_Expand(data)))
    return info.LastData


def Dir(targetdir, *data):
    '''Dir(targetdir: str[, data1, data2, ...])
    Create dir data object'''

    info.LastData = datatype.DirDataType(targetdir, set(_Expand(data)))
    return info.LastData


def File(targetfile):
    '''File(targetfile: str)
    Create file data object'''

    info.LastData = datatype.FileDataType(targetfile)
    return info.LastData
