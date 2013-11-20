import os
import mavc.info as info
import mavc.interface as interface

# Builder system with a command line parser
class CommandBuilder(interface.BaseBuilder):
    def RunLine(self, string):
        status = 0
        buf = ''
        for char in string + ' ':
            if status == 0:
                # Ready
                if char == '"':
                    status = 2
                elif char == "'":
                    status = 3
                elif char in ' \r\n\t':
                    pass
                else:
                    status = 1
                    buf += char
            elif status == 1:
                if char in ' \r\n\t':
                    status = 0
                    self.Run(buf)
                    buf = ''
                else:
                    buf += char
            elif status == 2:
                if char == '"':
                    if buf != '' and buf[-1] == '\\':
                        buf = buf[:-1] + '"'
                    else:
                        status = 0
                        self.Run(buf)
                        buf = ''
                else:
                    buf += char
            elif status == 3:
                if char == "'":
                    if buf != '' and buf[-1] == '\\':
                        buf = buf[:-1] + "'"
                    else:
                        status = 0
                        self.Run(buf)
                        buf = ''
                else:
                    buf += char

# Implementation of the builder system
class ImplBuilder(CommandBuilder):
    def __init__(self):
        pass

    def Run(self, command):
        print(command)
        if command == 'scan':
            pass
        elif command == 'add':
            pass
