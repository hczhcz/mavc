'''Functions that return data objects but not just constructors'''

import os
import re
from mavc import info
from mavc import datatype as coredatatype
import datatype


def Walk(target = os.curdir, ignore = info.IgnoreRule):
    '''Walking and create data objects
    Select path and file using skipping rule (regular expression or function)
    Return a set'''

    # Compile the ignore rule
    # Regular expression to lambda
    if isinstance(ignore, str):
        ReObject = re.compile(ignore)
        ignore = ReObject.match

    info.Log.Message('Scanning dir ' + target)

    Result = set()

    if not os.path.isdir(target):
        info.Log.Error('Not a dir ' + target)

    # Scan the list
    for item in os.listdir(target):
        NewPath = os.path.join(target, item)

        # Checking
        if not ignore(NewPath):
            info.Log.Message('Accepted path ' + NewPath)
            if os.path.isdir(NewPath):
                # Is dir
                Result.add(datatype.Dir(item, Walk(NewPath, ignore)))
            elif os.path.isfile(NewPath):
                # Is file
                Result.add(datatype.File(item))

    info.LastData = Result
    return info.LastData


def Continue(task, data):
    '''Append to an existing task data object'''

    if isinstance(task, coredatatype.TaskDataType):
        task.Data().append(data)
        info.LastData = task
    else:
        info.Log.Error('Not a task')

    return info.LastData
