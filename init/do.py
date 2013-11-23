import mavc.info as info
import mavc.module as module
from dirinit import *

def Init():
    # A MultiLog() as the root of the log system
    info.Log = module.MultiLog()

    # Print to console by default
    # info.Log.RegLog(module.ConsoleLog())
    info.Log.RegLog(module.SimpleConsoleLog())

    # Print startup information
    info.Log.Message('Hello, imagination')
    info.Log.Hint(info.FullName)
    info.Log.Hint('Version ' + info.Version)

    # Initialization tool dirs
    EnsureAllDir()

    # The lock system
    info.Lock = module.FileLock()

    # The database system
    # Pickle and Zlib used by default
    info.Database = module.PickleZlibDB()
