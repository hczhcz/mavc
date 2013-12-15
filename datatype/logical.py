from mavc import info
import abstract

class PackageDataType(abstract.CommentDataType, abstract.SetDataType):
    '''Package, contains multiple data
    Stored as a set, members are unique and not ordered'''

    def __init__(self, comment, data):
        self._SetComment(comment)
        self._SetData(data)
        info.Log.Progress(self.AsStr())

    def AsStr(self):
        return 'Package ' + self._Comment

    def AsCode(self):
        return 'PackageDataType(' + self._Comment + ', ' + repr(self._Data) + ')'

class CommitDataType(abstract.CommentDataType, abstract.SetDataType):
    '''Commit, like a package but with a time stamp
    Use current time in default format if time is not given'''

    _Time = ''

    def __init__(self, comment, data, time = ''):
        self._SetComment(comment)
        self._SetData(data)
        # Auto generate time if necessary
        if isinstance(time, str):
            if time == '':
                time = info.TimeInFormat()
                info.Log.Hint('Time of commit is ' + time)
            self._Time = time
        else:
            info.Log.InternalError('Time must be text')
        info.Log.Progress(self.AsStr())

    def AsStr(self):
        return 'Commit ' + self._Comment

    def AsCode(self):
        return 'CommitDataType(' + self._Comment + ', ' + repr(self._Data)\
            + self._Time + ')'

class TaskDataType(abstract.CommentDataType, abstract.ListDataType):
    '''Task, contains multiple data
    Stored as an ordered list'''

    def __init__(self, comment, data):
        self._SetComment(comment)
        self._SetData(data)
        info.Log.Progress(self.AsStr())

    def AsStr(self):
        return 'Task ' + self._Comment

    def AsCode(self):
        return 'TaskDataType(' + self._Comment + ', ' + repr(self._Data) + ')'
