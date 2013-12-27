'''The implementation of the log system'''

from mavc import info
from mavc import interface


class TextLog(interface.BaseLog):
    '''Log expressed in plain text
    Override AddText() method to implement
    Log message should be English text string'''

    def _AddText(self, title, text):
        '''Receive text and do something (print, write to file, etc)'''

        pass

    def Progress(self, msg):
        self._AddText('Progress', msg)
        super(TextLog, self).Progress(msg)

    def Message(self, msg):
        self._AddText('Message', msg)
        super(TextLog, self).Message(msg)

    def Hint(self, msg):
        self._AddText('Hint', msg)
        super(TextLog, self).Hint(msg)

    def Error(self, msg):
        self._AddText('Error', msg)
        super(TextLog, self).Error(msg)

    def InternalError(self, msg):
        self._AddText('Internal error', msg)
        super(TextLog, self).InternalError(msg)


class ConsoleLog(TextLog):
    '''Implementation of the log system, to print log to console
    Use standard IO
    ISO time format'''

    def _AddText(self, title, text):
        # Check if input is string
        if not isinstance(title, str):
            # title = 'Unknown'
            title = 'InternalError'
        if not isinstance(text, str):
            text = str(text)
        print(info.TimeInFormat() + ' ' + title + ': ' + text)


class SimpleConsoleLog(TextLog):
    '''Implementation of the log system
    Like CinsoleLog but print important log only
    No time information'''

    def Message(self, msg):
        '''Ignore message'''

        # super(TextLog, self).Message(msg)
        pass

    def _AddText(self, title, text):
        # Check if input is string
        if not isinstance(title, str):
            # title = 'Unknown'
            title = 'InternalError'
        if not isinstance(text, str):
            text = str(text)
        print(title + ': ' + text)


class MultiLog(object):
    '''A wrapper to use multiple log system
    use RegLog() to add class of log'''

    _LogList = set()

    def __getattr__(self, name):
        '''Iterate the list when a method is called'''

        def DynamicCall(msg):
            '''Make a closure to apply the call'''

            for item in self._LogList:
                getattr(item, name)(msg)

        return DynamicCall

    def RegLog(self, log):
        '''Add to the list
        Only accept log object'''

        if isinstance(log, interface.BaseLog):
            self._LogList.add(log)

    def Clear(self):
        '''Clear the list of log object'''

        self._LogList.clear()
