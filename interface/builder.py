import mavc.info as info

# Base class of the data builder system
# To parse commands and create data (see datatype module)
# Abstract, override methods to impletment this class
class BaseBuilder(object):
    def __init__(self):
        info.Log.InternalError('Abstract builder can not be initialized')

    # Run a command
    def Run(self, command):
        pass

    # Split a string and call Run()
    def RunLine(self, string):
        pass

    # Run a command when a method is called
    def __getattr__(self, name):
        # Make a closure to apply the call
        def DynamicCall():
            self.Run(name)

        return DynamicCall
