'''The log system, to log and show messages'''


class BaseLog(object):
    '''Base class of the log system
    Error (and internal error) will cause a Python exception
    Abstract, override methods to impletment this class'''

    def Progress(self, msg):
        '''Progress, what has done, good news'''

        pass

    def Message(self, msg):
        '''Message, verbose information
        For debugging or some special usage'''

        pass

    def Hint(self, msg):
        '''Hint, unusual things
        The progress can still continue'''

        pass

    def Error(self, msg):
        '''Error, dangerous things, bad news
        The progress can not continue'''

        assert(False)

    def InternalError(self, msg):
        '''Internal error, bad things happen in the system
        For software bug or internal bad data
        The progress can not continue'''

        assert(False)

    def __getattr__(self, name):
        '''Send unknown call to internal error'''

        return self.InternalError
