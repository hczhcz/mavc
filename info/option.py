import os
import datetime

# Do not change if database is already created

# Readable mode
# Make the database readable
ReadableMode = False

# Working dir
WorkingDir = ''

# Allow binary database, not readable but effective
# If false, the database system will use plain text
BinaryStore = not ReadableMode

# Compress the database
# The same as BinaryStore would be good
DoCompress = BinaryStore

# Zlib compression level (0 to 9)
CompressLevel = 6

# Format of time, ISO by default
TimeInFormat = lambda: datetime.datetime.now().isoformat()

# Check file and dir name
IsDirFile = lambda x: not set(x) <= {'.', '*', '?', '+'} and not os.sep in x
