import mavc.info as info

# Base class of data
# Abstract, override methods to impletment this class
class BaseDataType(object):
    def __init__(self):
        info.Log.InternalError('Abstract data can not be initialized')

    # Version, for compatibility checking, check by database system
    DataVer = info.Version

    # Called on database pushing
    def OnPush(self, target):
        pass

    # Called on database pulling
    # Do action such as file IO
    def OnPull(self, target):
        pass

    # Return a set of identifier that needed (referred) by this object
    # For defragment only, work with Pull(..., doaction = False)
    def Ref(self):
        pass

    # Return a set like Ref() and do recursion call
    def AllRef(self):
        pass
