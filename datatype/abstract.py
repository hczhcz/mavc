from mavc import info
import storable

class RawDataType(storable.StorableDataType):
    '''Raw data
    Can store almost anything
    For debug only'''

    _Data = None

    def __init__(self, data):
        info.Log.Progress('Raw data ' + str(data))
        info.Log.Hint('Raw data type for debug only')
        self._Data = data

    def Data(self):
        return self._Data

    def _DoOnPush(self, target):
        info.Log.Message('Push ' + str(self._Data))

    def _DoOnPull(self, target):
        info.Log.Message('Pull ' + str(self._Data))

    def _DoRef(self):
        return set()

class CommentDataType(storable.StorableDataType):
    '''Data with comment
    Comment should be string'''

    _Comment = ''

    # As string, return comment
    # def __str__(self):
    #     return self._Comment

    def _SetComment(self, comment):
        if isinstance(comment, str):
            self._Comment = comment
        else:
            info.Log.InternalError('Comment must be text')

    def Comment(self):
        return self._Comment

class SetDataType(storable.StorableDataType):
    '''Unique list (set) of identifier
    Check type of input data'''

    _Data = set()
    _IDData = set()

    def _SetData(self, data):
        if isinstance(data, set):
            for item in data:
                if not isinstance(item, storable.StorableDataType):
                    info.Log.InternalError('Wrong identifier in the set')
            self._Data = data
        else:
            info.Log.InternalError('Input is not a set')

    def Data(self):
        return self._Data

    def _DoOnPush(self, target):
        info.Log.Message('Push a set')
        self._IDData = {
            info.Database.Push(item, True, target) for item in self._Data
        }
        self._Data = set()

    def _DoOnPull(self, target):
        info.Log.Message('Pull a set')
        self._Data = {
            info.Database.Pull(item, True, target) for item in self._IDData
        }
        self._IDData = set()

    def _DoRef(self):
        return self._IDData

class ListDataType(storable.StorableDataType):
    '''Ordered list of identifier
    Check type of input data'''

    _Data = list()
    _IDData = list()

    def _SetData(self, data):
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, storable.StorableDataType):
                    info.Log.InternalError('Wrong identifier in the list')
            self._Data = data
        else:
            info.Log.InternalError('Input is not a list')

    def Data(self):
        return self._Data

    def _DoOnPush(self, target):
        info.Log.Message('Push a list')
        self._IDData = [
            info.Database.Push(item, True, target) for item in self._Data
        ]
        self._Data = list()

    def _DoOnPull(self, target):
        info.Log.Message('Pull a list')
        self._Data = [
            info.Database.Pull(item, True, target) for item in self._IDData
        ]
        self._IDData = list()

    def _DoRef(self):
        return self._IDData

class DirFileDataType(storable.StorableDataType):
    '''Dir or file
    Do IO when calling _DoOnPush() or _DoOnPull()'''

    _Target = ''

    def _CheckPath(self):
        if not info.IsDirFile(self._Target):
            info.Log.InternalError('Bad path ' + self._Target)

    def _SetTarget(self, target):
        if isinstance(target, str):
            self._Target = target
            self._CheckPath()
        else:
            info.Log.InternalError('Path must be text')

    def Target(self):
        self._CheckPath()
        return self._Target
