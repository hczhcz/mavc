'''Actions to do'''

from mavc import info


def Push(data = None, lock = False, target = ''):
    '''Push data to the database'''

    if data is None:
        data = info.LastData

    info.LastData = info.Database.Push(data, True, target)

    if lock:
        info.Lock.Lock(info.LastData)

    return info.LastData


def Pull(identifier = None, unlock = False, target = ''):
    '''Pop data from the database'''

    if identifier is None:
        identifier = info.LastData

    if unlock:
        info.Lock.Unlock(identifier)

    info.LastData = info.Database.Pull(identifier, True, target)

    return info.LastData


def Write(data = None, target = ''):
    '''Push data to the database without doing action'''

    if data is None:
        data = info.LastData

    info.LastData = info.Database.Push(data, False, target)

    return info.LastData


def Read(identifier = None, target = ''):
    '''Pop data from the database without doing action'''

    if identifier is None:
        identifier = info.LastData

    info.LastData = info.Database.Pull(identifier, False, target)

    return info.LastData


def Lock(identifier = None):
    '''Lock an identifier'''

    if identifier is None:
        identifier = info.LastData

    info.Lock.Lock(identifier)
    return identifier


def Unlock(identifier = None):
    '''Unlock an identifier'''

    if identifier is None:
        identifier = info.LastData

    info.Lock.Unlock(identifier)
    return identifier


def List():
    '''List all locked data'''

    return info.Database.PullLocked()
