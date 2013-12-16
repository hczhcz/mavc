'''Check and create tool dirs'''

import os
from mavc import info

def _EnsureDir(targetdir):
    '''Check tool dir and initialize if necessary'''

    if not os.path.isdir(targetdir):
        info.Log.Hint('Tool dir need to create ' + targetdir)
        try:
            os.mkdir(targetdir)
        except:
            info.Log.Error('Can not create tool dir ' + targetdir)

def EnsureAllDir():
    '''Call _EnsureDir() to check all tool dirs'''

    for item in info.AllToolDir:
        _EnsureDir(item)
