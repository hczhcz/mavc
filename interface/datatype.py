import mavc.info as info

# Base class of data
# Abstract, override methods to impletment this class
class BaseDataType(object):
    # Version, for compatibility checking, check by database system
    DataVer = info.Version

    # If data stored, be True after OnPush() and before OnPull()
    _Stored = False

    def __init__(self):
        info.Log.InternalError('Abstract data can not be initialized')

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

    # Called on database pushing
    def OnPush(self):
        if not self._Stored:
            self._Stored = True
            self._DoOnPush()
        else:
            info.Log.InternalError('Can not push stored data')

    # Called on database pulling
    # Do action such as file IO
    def OnPull(self):
        if self._Stored:
            self._Stored = False
            self._DoOnPull()
        else:
            info.Log.InternalError('Can not pull restored data')

    # Return a set of identifier that needed (referred) by this object
    # For defragment only, work with Pull(..., doaction = False)
    def Ref(self):
        if self._Stored:
            return set(self._DoRef())
        else:
            info.Log.InternalError('Can not read identifier from restored data')
