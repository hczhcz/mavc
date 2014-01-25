'''Misc functions'''

from mavc import info
from mavc import init


def Last():
    '''Last()
    Last generated data object or identifier'''

    return info.LastData


def GarbageCollection():
    '''GarbageCollection()
    Do garbage collection'''

    info.Database.GarbageCollection()


def Repl():
    '''Repl()
    Run an interactive console'''

    return init.Repl(info.Globals)


def Help(target):
    '''Help(target: func/obj)
    Print doc string, wrapper of __doc__'''

    print(target.__doc__)


def Exit():
    '''Exit()
    Exit, wrapper of exit(), useful in REPL'''

    exit()
