'''Main script, to run a REPL (interactive console)'''

import sys
import os

# Load as mavc module
sys.path.append(os.path.join(sys.path[0], os.pardir))
from mavc import *

init.Repl(info.Globals)
