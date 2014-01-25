'''Data objects, to contain data, can be stored in the database'''

from mavc import info


class BaseDataType(object):
    '''Base class of data
    Abstract, override methods to impletment this class'''

    def __init__(self):
        info.Log.InternalError('Abstract data can not be initialized')

    # Version, for compatibility checking, check by database system
    DataVer = info.Version

    def __str__(self):
        '''Cast data as string'''

        if info.DeepObjStr:
            return self.AsStrDeep()
        else:
            return self.AsStr()

    def __repr__(self):
        '''Repr data as string'''

        if info.FriendlyRepr:
            return str(self)
        else:
            return self.AsCode()

    def AsStrDeep(self, front = ''):
        '''Return data as readable string, include children's data'''

        # return front + self.AsStr() + '\n'\
        #     + front + info.DeepObjStrHead + str(self.__dict__)
        return front + self.AsStr()

    def AsStr(self):
        '''Return data as readable string'''

        return 'Data ' + self.__class__.__name__

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
        For GC only, work with Pull(..., doaction = False)'''

        pass

    def AllRef(self):
        '''Return a set like Ref() and do recursion call'''

        pass
