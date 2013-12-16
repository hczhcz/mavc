'''REPL, an interactive console'''

import code

def Repl(target):
    '''Run a REPL (interactive console) with local variables'''

    code.InteractiveConsole(target).interact(r'''
 --------------------------
| MAVC Interactive Console |
 --------------------------''')
