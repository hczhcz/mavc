import sys
sys.modules['mavc'] = sys.modules[__name__]
del sys

import info
import interface
import datatype
import module
import init
import front
from front import *

init.Init()

if __name__ == '__main__':
    init.Repl(globals())
