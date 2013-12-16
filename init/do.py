'''Initializer of the whole system'''

from mavc import info
from mavc import module
import dirinit

def Init():
    '''Do initialization of the whole system'''

    # A MultiLog() as the root of the log system
    info.Log = module.MultiLog()

    # Print to console by default
    if info.Verbose:
        info.Log.RegLog(module.ConsoleLog())
    else:
        info.Log.RegLog(module.SimpleConsoleLog())

    # Print startup information
    info.Log.Message('Hello, imagination')
    info.Log.Hint(info.FullName)
    info.Log.Hint('Version ' + info.Version)

    # Initialize tool dirs
    dirinit.EnsureAllDir()

    # The lock system
    info.Lock = module.FileLock()

    # The database system
    # Pickle and Zlib used by default
    info.Database = module.PickleZlibDB()
