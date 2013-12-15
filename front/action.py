from mavc import info

def Push(data, target = ''):
    '''Push data to the database'''

    info.Database.Push(data, True, target)

def Pull(identifier, target = ''):
    '''Pop data from the database'''

    info.Database.Pull(identifier, True, target)

def Write(data, target = ''):
    '''Push data to the database without doing action'''

    info.Database.Push(data, False, target)

def Read(identifier, target = ''):
    '''Pop data from the database without doing action'''

    info.Database.Pull(identifier, False, target)

def List():
    '''TODO, list all locked'''
    '''TODO: add tag system

    example:
    .mavc/tags/master = '0x12345678'
    .mavc/tags/release1 = '0x23456789'
    '''

    pass

def Exit():
    '''Exit, wrapper of exit(), useful in REPL'''

    exit()
