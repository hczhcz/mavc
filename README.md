MAVC
====

A Python-based lightweight revision control system.

Run as REPL
----

Just run `python mavc` (the path of MAVC) or `python __main__.py`.

Install MAVC
----

Copy files to dir `mavc` under Python's search path (this is usually `/usr/local/lib/python`).

Then, you can `import mavc` in Python.

Usage
----

Import the module:

    >>> import mavc
    Hint: Maybe Another Version Control
    Hint: Version 1.0.0

Functions:

    >>> dir(mavc)
    ['Commit', 'CommitTimed', 'Dir', 'Exit', 'File', 'GarbageCollection', 'Help', 'Last', 'List', 'Lock', 'Package', 'Pull', 'Push', 'Read', 'Repl', 'Submit', 'SubmitDB', 'Task', 'Unlock', 'Walk', 'Write', ...]

Add files and dirs:

    >>> from mavc import *
    >>> Dir('foo', File('bar'))
    Progress: File bar
    Progress: Dir foo
    Dir foo
        File bar

Or scan dirs and files (you can also ignore some files):

    >>> Walk('.')
    Progress: File baz
    Progress: File bar
    Progress: Dir foo
    set([Dir foo
        File bar
        File baz])
    >>> Walk('.', '.*z')
    Progress: File bar
    Progress: Dir foo
    set([Dir foo
        File bar])
    >>> Walk('.', '.*b..')
    Progress: Dir foo
    set([Dir foo])

Packages (not necessary):

    >>> Walk('.')
    ...
    >>> Package('pkg1', Last())
    Progress: Package pkg1
    Package pkg1
        Dir foo
            File bar
            File baz

`Last()` can be omitted. `Package('pkg1')` is ok.

Committing (in memory, not stored in the database):

    >>> Commit('update the pkg1', Last())
    Hint: Time of commit is 2014-01-01T00:00:00.000000
    Progress: Commit update the pkg1
    Commit update the pkg1
        Package pkg1
            Dir foo
                File bar
                File baz

If you want to set the timestamp manually:

    >>> import datetime
    >>> CommitTimed('test', datetime.datetime.now().isoformat())
    Progress: Commit test
    Commit test
        ...

Create a task.

    >>> t = Task('release', [])
    Progress: Task release

Commit and add to a task:

    >>> Commit('add files', Walk('.'))
    Progress: File baz
    Progress: File bar
    Progress: Dir foo
    Hint: Time of commit is 2014-01-01T00:00:00.000000
    Progress: Commit add files
    Commit add files
        ...
    >>> Submit(t)
    Task release
        Commit add files
            ...

Now you created some data objects. Then you can store them.

Store data into the local database (dir `./.mavc`):

    >>> Push(t)
    Progress: Database stored 0x11111111
    Progress: Database stored 0x22222222
    Progress: Database stored 0x33333333
    Progress: Database stored 0x44444444
    Progress: Database stored 0x55555555
    '0x55555555'

`0x55555555` is the identifier of `Task('release')`.

If SHA-1 hash function is enabled (see `info/option.py`), the identifier will be much longer.

Restore data:

    >>> Pull()
    Progress: Data restored 0x11111111
    Progress: Data restored 0x22222222
    Progress: Data restored 0x33333333
    Progress: Data restored 0x44444444
    Progress: Data restored 0x55555555
    Task release
        Commit add files
            ...

`Pull()`, `Pull('0x55555555')` and `Pull(Last())` are the same here.

Besides, `Write()` is `Push()` without reading file, and `Read()` is `Pull()` without writting file.

Update a task from the database:

    >>> Push(Task('dev', Commit('init', File('foo'))))
    ...
    '0x66666666'
    >>> SubmitDB('0x66666666', Commit('test', File('bar')))
    ...
    '0x77777777'
    >>> Pull().Data()
    ...
    [Commit init, Commit test]

Data is stored in `.../.mavc`.

Lock data so that it will not be deleted (see `GarbageCollection()`):

    >>> Lock()
    Progress: Locked 0x55555555 to 1
    '0x55555555'

Unlock:

    >>> Unlock()
    Progress: Unlocked 0x55555555 to 0
    '0x55555555'

List all locked:

    >>> List()
    set([Task release])

And...

    >>> GarbageCollection()
    Hint: Total garbage 0
    Progress: GC finished
    >>> Repl()
    
     --------------------------
    | MAVC Interactive Console |
     --------------------------
    >>> # Repl() is useful in scripts
    >>> Help(List)
    'List all locked data'
    >>> Exit()

Use in scripts
----

Script file:

    from mavc import *
    
    Dir('foo', File('bar'), File('baz'))
    Package('pkg1')
    Repl()

Rename it as `.mavc_scan.py`.

Run it:

    Hint: Maybe Another Version Control
    Hint: Version 1.0.0
    Progress: File bar
    Progress: File baz
    Progress: Dir foo
    Progress: Package pkg1
    
     --------------------------
    | MAVC Interactive Console |
     --------------------------
    >>> Last()
    Package pkg1
        Dir foo
            File bar
            File baz
    >>> Commit('update the pkg1')
    Hint: Time of commit is 2014-01-01T00:00:00.000000
    Progress: Commit update the pkg1
    Commit update the pkg1
        Package pkg1
            Dir foo
                File bar
                File baz
    >>> Lock(Push())
    ...
    >>> Exit()
