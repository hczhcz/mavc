from mavc import info

# Base class of the lock system
# Lock should be additive (two lock need two unlock)
# Abstract, override methods to impletment this class
class BaseLock(object):
    def __init__(self):
        info.Log.InternalError('Abstract lock can not be initialized')

    # Lock an identifier
    def Lock(self, identifier):
        pass

    # Unlock an identifier
    def Unlock(self, identifier):
        pass

    # Return a set of identifier that locked
    def AllLocked(self):
        pass
