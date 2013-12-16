'''Storable data, base of data object'''

from mavc import info
from mavc import interface

class StorableDataType(interface.BaseDataType):
    '''Storable data
    Use flag _Stored to mark'''

    # If data stored, be True after OnPush() and before OnPull()
    _Stored = False

    def _DoOnPush(self, target):
        '''Called by OnPush()
        Do action such as file IO'''

        pass

    def _DoOnPull(self, target):
        '''Called by OnPull()
        Do action such as file IO'''

        pass

    def _DoRef(self):
        '''Called by Ref()
        Return all needed identifier
        Do not keep any identifier before OnPush() or after OnPull()
        Return an empty set if nothing to return'''

        pass

    def OnPush(self, target):
        if not self._Stored:
            self._Stored = True
            self._DoOnPush(target)
        else:
            info.Log.InternalError('Can not push stored data')

    def OnPull(self, target):
        if self._Stored:
            self._Stored = False
            self._DoOnPull(target)
        else:
            info.Log.InternalError('Can not pull restored data')

    def Ref(self):
        if self._Stored:
            return set(self._DoRef())
        else:
            info.Log.InternalError('Can not read identifier from restored data')

    def AllRef(self):
        Result = set()

        def AppendRef(item):
            '''Append items to the reference list'''

            if not item in Result:
                Result.add(item)
                Ref = info.Database.Pull(item, False, None).Ref()
                for refitem in Ref:
                    AppendRef(refitem)

        for item in self.Ref():
            AppendRef(item)

        return Result
