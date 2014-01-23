'''Actions to do'''

from mavc import info


def Push(data = None, target = ''):
    '''Push data to the database'''

    if data is None:
        data = info.LastData

    return info.Database.Push(data, True, target)


def Pull(identifier, target = ''):
    '''Pop data from the database'''

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
