if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath('.'))
    from mavc import *
    del os
    del sys

    init.Repl(globals())
else:
    import info
    import interface
    import datatype
    import module
    import init
    import front
    from front import *

    init.Init()
