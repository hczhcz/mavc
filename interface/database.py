'''The database system, to store data'''

from mavc import info


class BaseDB(object):
    '''Base class of the database system
    Abstract, override methods to impletment this class'''

    def __init__(self):
        info.Log.InternalError('Abstract database can not be initialized')

    def Push(self, data, doaction, target):
        '''Push data to the database
        Return identifier
        Set doaction = True to call OnPush()'''

        pass

    def Pull(self, identifier, doaction, target):
        '''Pull data from the database
        Return data
        Set doaction = True to call OnPull()'''

        pass

    def PullLocked(self):
        '''Pull all locked data but not call OnPull()
        Return a set of data'''

        pass

    def GarbageCollection(self):
        '''Delete unaccessable data in the database'''

        pass
