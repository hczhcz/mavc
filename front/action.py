'''Actions to do'''

from mavc import info


def Push(data = None, lock = False, target = ''):
    '''Push data to the database'''

    if data is None:
        data = info.LastData

    identifier = info.Database.Push(data, True, target)

    if lock:
        info.Lock.Lock(identifier)

    return identifier


def Pull(identifier, unlock = False, target = ''):
    '''Pop data from the database'''

    if unlock:
        info.Lock.Unlock(identifier)

    info.LastData = info.Database.Pull(identifier, True, target)

    return info.LastData


def Write(data = None, target = ''):
    '''Push data to the database without doing action'''

    if data is None:
        data = info.LastData

    return info.Database.Push(data, False, target)


def Read(identifier, target = ''):
    '''Pop data from the database without doing action'''

    info.LastData = info.Database.Pull(identifier, False, target)

    return info.LastData


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
