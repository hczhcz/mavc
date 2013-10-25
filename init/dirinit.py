import os
import mavc.info as info

# Check tool dir and initialize if necessary
def _EnsureDir(dir):
    if not os.path.exists(dir):
        info.Log.Hint('Tool dir need to create ' + dir)
        try:
            os.mkdir(dir)
        except:
            info.Log.Error('Can not create tool dir ' + dir)

# Call _EnsureDir() to check all tool dirs
def EnsureAllDir():
    for item in info.AllToolDir:
        _EnsureDir(item)
