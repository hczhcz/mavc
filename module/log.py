import mavc.info as info
import mavc.interface as interface

# Log expressed in plain text
# Override AddText() method to implement
# Log message should be English text string
class TextLog(interface.BaseLog):
    # Receive text and do something (print, write to file, etc)
    def _AddText(self, title, text):
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

    # def Warning(self, msg):
    #     self._AddText('Warning', msg)
    #     super(TextLog, self).Warning(msg)

    def Error(self, msg):
        self._AddText('Error', msg)
        super(TextLog, self).Error(msg)

    def InternalError(self, msg):
        self._AddText('Internal error', msg)
        super(TextLog, self).InternalError(msg)

# Implementation of the log system, to print log to console
# Use standard IO
# ISO time format
class ConsoleLog(TextLog):
    def _AddText(self, title, text):
        # Check if input is string
        if not isinstance(title, str):
            # title = 'Unknown'
            title = 'InternalError'
        if not isinstance(text, str):
            text = str(text)
        print(info.TimeInFormat() + ' ' + title + ': ' + text)

# Implementation of the log system
# Like CinsoleLog but print important log only
# No time information
class SimpleConsoleLog(TextLog):
    def Message(self, msg):
        # Ignore message
        super(TextLog, self).Message(msg)

    def _AddText(self, title, text):
        # Check if input is string
        if not isinstance(title, str):
            # title = 'Unknown'
            title = 'InternalError'
        if not isinstance(text, str):
            text = str(text)
        print(title + ': ' + text)

# A wrapper to use multiple log system
# use RegLog() to add class of log
class MultiLog(object):
    _LogList = set()

    # Iterate the list when a method is called
    def __getattr__(self, name):
        # Make a closure to apply the call
        def DynamicCall(msg):
            for item in self._LogList:
                getattr(item, name)(msg)

        return DynamicCall

    def RegLog(self, log):
        # Only accept log type
        if isinstance(log, interface.BaseLog):
            self._LogList.add(log)

    def Clear(self):
        self._LogList.clear()
