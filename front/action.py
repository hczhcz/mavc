'''Actions to do'''

from mavc import info


def Push(data, target = ''):
    '''Push data to the database'''

    return info.Database.Push(data, True, target)


def Pull(identifier, target = ''):
    '''Pop data from the database'''

    return info.Database.Pull(identifier, True, target)


def Write(data, target = ''):
    '''Push data to the database without doing action'''

    return info.Database.Push(data, False, target)


def Read(identifier, target = ''):
    '''Pop data from the database without doing action'''

    return info.Database.Pull(identifier, False, target)


def Lock(identifier):
    '''Lock an identifier'''

    info.Lock.Lock(identifier)
    return identifier


def Unlock(identifier):
    '''Unlock an identifier'''

    info.Lock.Unlock(identifier)
    return identifier


def List():
    '''List all locked data'''

    return info.Database.PullLocked()


def Exit():
    '''Exit, wrapper of exit(), useful in REPL'''

    exit()
