'''Base information and system modules'''

# MAVC
FullName = 'Maybe Another Version Control'
Version = '1.3.0'

# Check compatible version
Compatible = lambda ver: ver in {'1.3.0'}

# Modules, initialize later
Log = None
Lock = None
Database = None

# The namespace of the frontend
Globals = None
