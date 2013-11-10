import mavc.info as info
import mavc.interface as interface

# Storable data
# Use flag _Stored to mark
class StorableDataType(interface.BaseDataType):
    # If data stored, be True after OnPush() and before OnPull()
    _Stored = False

    # Called by OnPush()
    # Do action such as file IO
    def _DoOnPush(self):
        pass

    # Called by OnPull()
    # Do action such as file IO
    def _DoOnPull(self):
        pass

    # Called by Ref()
    # Return all needed identifier
    # Do not keep any identifier before OnPush() or after OnPull()
    # Return an empty set if nothing to return
    def _DoRef(self):
        pass

    def OnPush(self):
        if not self._Stored:
            self._Stored = True
            self._DoOnPush()
        else:
            info.Log.InternalError('Can not push stored data')

    def OnPull(self):
        if self._Stored:
            self._Stored = False
            self._DoOnPull()
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
            if not item in Result:
                Result.add(item)
                Ref = info.Database.Pull(item, False).Ref()
                for refitem in Ref:
                    AppendRef(refitem)

        for item in self.Ref():
            AppendRef(item)

        return Result
