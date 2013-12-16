'''Data objects, to contain data, can be stored in the database'''

from mavc import info

class BaseDataType(object):
    '''Base class of data
    Abstract, override methods to impletment this class'''

    def __init__(self):
        info.Log.InternalError('Abstract data can not be initialized')

    # Version, for compatibility checking, check by database system
    DataVer = info.Version

    def __repr__(self):
        '''Repr data as string'''

        return self.AsStr() if info.FriendlyRepr else self.AsCode()

    def __str__(self):
        '''Cast data as string'''

        return self.AsStr()

    def AsStr(self):
        '''Return data as readable string'''

        return 'Data ' + self.__class__.__name__ + ' ' + str(self.__dict__)

    def AsCode(self):
        '''Return data as code string'''

        return self.__class__.__name__ + '()'

    def OnPush(self, target):
        '''Called on database pushing'''

        pass

    def OnPull(self, target):
        '''Called on database pulling
        Do action such as file IO'''

        pass

    def Ref(self):
        '''Return a set of identifier that needed (referred) by this object
        For defragment only, work with Pull(..., doaction = False)'''

        pass

    def AllRef(self):
        '''Return a set like Ref() and do recursion call'''

        pass
