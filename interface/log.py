# Base class of the log system
# Error (and internal error) will cause a Python exception
# Abstract, override methods to impletment this class
class BaseLog(object):
    def Progress(self, msg):
        pass

    def Message(self, msg):
        pass

    def Hint(self, msg):
        pass

    # No warning, anything unsafe is error
    # def Warning(self, msg):
    #     pass

    def Error(self, msg):
        assert(False)

    def InternalError(self, msg):
        assert(False)

    def __getattr__(self, name):
        # Send unknown call to internal error
        return self.InternalError
