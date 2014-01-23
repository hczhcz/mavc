'''Information about the database system'''

import os
import option

# Tool dirs
# Also need to be added in AllToolDir

# The root dir
# Hidden by default
RootDir = ('_mavc' if option.ReadableMode else '.mavc')

# The dir name of database
StoreDir = os.path.join(RootDir, 'data')

# The dir name of garbage file
GarbageDir = os.path.join(RootDir, 'garbage')

# The dir name of lock
LockDir = os.path.join(RootDir, 'lock')

# The dir name of output buffer
OutputDir = os.path.join(RootDir, 'output')

# The dir name of backup
BackupDir = os.path.join(RootDir, 'backup')

# List of all tool dirs
# Sorted by creation order
AllToolDir = [RootDir, StoreDir, GarbageDir, LockDir, OutputDir, BackupDir]

# Temporary data identifier
IDTemp = 'temp'
