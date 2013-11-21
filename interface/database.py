import mavc.info as info

# Base class of the database system
# Abstract, override methods to impletment this class
class BaseDB(object):
    def __init__(self):
        info.Log.InternalError('Abstract database can not be initialized')

    # Push data to the database
    # Return identifier
    # Set doaction = True to call OnPush()
    def Push(self, data, doaction = True):
        pass

    # Pull data from the database
    # Return data
    # Set doaction = True to call OnPull()
    def Pull(self, id, doaction = True):
        pass

    # Pull all locked data but not call OnPull()
    # Return a set of data
    def PullLocked(self):
        pass

    # Delete unaccessable data in the database
    def Defrag(self):
        pass
