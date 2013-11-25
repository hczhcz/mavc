from mavc import info
import abstract

class PackageDataType(abstract.CommentDataType, abstract.SetDataType):
    def __init__(self, comment, data):
        info.Log.Progress('Package ' + comment)
        self._SetComment(comment)
        self._SetData(data)

class CommitDataType(abstract.CommentDataType, abstract.SetDataType):
    _Time = ''

    def __init__(self, comment, data, time = ''):
        info.Log.Progress('Commit ' + comment)
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

class TaskDataType(abstract.CommentDataType, abstract.ListDataType):
    def __init__(self, comment, data):
        info.Log.Progress('Task ' + comment)
        self._SetComment(comment)
        self._SetData(data)
