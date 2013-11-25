import os
import option

# Tool dirs
# Also need to be added in AllToolDir

# The root dir
# Hidden by default
RootDir = ('_mavc' if option.ReadableMode else '.mavc') + os.sep

# The dir name of database
StoreDir = RootDir + 'data' + os.sep

# The dir name of frag file
FragDir = RootDir + 'frag' + os.sep

# The dir name of lock
LockDir = RootDir + 'lock' + os.sep

# The dir name of output buffer
OutputDir = RootDir + 'output' + os.sep

# The dir name of backup
BackupDir = RootDir + 'backup' + os.sep

# List of all tool dirs
# Sorted by creation order
AllToolDir = [RootDir, StoreDir, FragDir, LockDir, OutputDir, BackupDir]

# Temporary data identifier
IDTemp = 'temp'
