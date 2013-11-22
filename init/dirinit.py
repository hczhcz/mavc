import os
import mavc.info as info

# Check tool dir and initialize if necessary
def _EnsureDir(targetdir):
    if not os.path.isdir(targetdir):
        info.Log.Hint('Tool dir need to create ' + targetdir)
        try:
            os.mkdir(targetdir)
        except:
            info.Log.Error('Can not create tool dir ' + targetdir)

# Call _EnsureDir() to check all tool dirs
def EnsureAllDir():
    for item in info.AllToolDir:
        _EnsureDir(item)
