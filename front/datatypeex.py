import os
import re
from mavc import info
import datatype

def Last():
    '''Last generated data object'''

    return info.LastData

def Walk(target, ignore = r'.*' + os.sep + r'\..*'):
    '''Walking and create data objects
    Select path and file using ignore rule (regular expression or function)
    Return a set'''

    # Compile the ignore rule
    # Regular expression to lambda
    if isinstance(ignore, str):
        ReObject = re.compile(ignore)
        ignore = lambda x: ReObject.match(x)

    info.Log.Message('Scanning dir ' + target)

    Result = set()

    if not os.path.isdir(target):
        info.Log.Error('Not a dir ' + target)

    for item in os.listdir(target):
        NewPath = target + item

        # Checking
        if not ignore(NewPath):
            info.Log.Message('Accepted path ' + NewPath)
            if os.path.isdir(NewPath):
                # Is dir
                Result.add(datatype.Dir(item, Walk(NewPath + os.sep, ignore)))
            elif os.path.isfile(NewPath):
                # Is file
                Result.add(datatype.File(item))

    return Result
