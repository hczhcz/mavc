import mavc.info as info

# Base class of data
# Abstract, override methods to impletment this class
class BaseDataType(object):
    # Version, for compatibility checking, check by database system
    DataVer = info.Version

    # Called on database pushing
    def OnPush(self):
        pass

    # Called on database pulling
    # Do action such as file IO
    def OnPull(self):
        pass

    # Return a set of identifier that needed (referred) by this object
    # For defragment only, work with Pull(..., doaction = False)
    def Ref(self):
        pass

    # Return a set like Ref() and do recursion call
    def AllRef(self):
        pass
