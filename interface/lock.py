from mavc import info

class BaseLock(object):
    '''Base class of the lock system
    Lock should be additive (two lock need two unlock)
    Abstract, override methods to impletment this class'''

    def __init__(self):
        info.Log.InternalError('Abstract lock can not be initialized')

    def Lock(self, identifier):
        '''Lock an identifier'''

        pass

    def Unlock(self, identifier):
        '''Unlock an identifier'''

        pass

    def AllLocked(self):
        '''Return a set of identifier that locked'''

        pass
