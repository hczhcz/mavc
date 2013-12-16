'''Main script, to run a REPL (interactive console)'''

import sys
import os

# Load as mavc module
sys.path.append(sys.path[0] + os.sep + os.pardir)
from mavc import *

del os
del sys

init.Repl(globals())
