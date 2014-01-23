'''Misc functions'''

from mavc import info
from mavc import init


def Last():
    '''Last generated data object'''

    return info.LastData


def Repl():
    '''Run an interactive console'''

    return init.Repl(info.Globals)


def Help(target):
    '''Return doc string, wrapper of __doc__'''

    return target.__doc__


def Exit():
    '''Exit, wrapper of exit(), useful in REPL'''

    exit()
