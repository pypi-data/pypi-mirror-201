try:
    import gnureadline as readline
except ImportError:
    import readline
import sys


# Use tab for completion
readline.parse_and_bind('tab: complete')


# Readline defaults to complete with local filenames. Definitely not what we
# want.

def null_complete(text, start):
    return None
readline.set_completer(null_complete)


# I'd like to bind a special key (like ctrl-del) to kill-whole-line, but I can't
# get it to work on my Mac in iTerm. So we're going to use ctrl-A for that.
# readline.parse_and_bind('"\C-a": kill-whole-line')


def rlinput(prompt:str="", default:str="", options:list=None):
    """
    Get input with preset default and/or tab completion of options

    Parameters:

    prompt:str - string to output before requesting input, same as in the
    input() function

    default:str - value with which to prepopulate the response, can be cleared
    with ctrl-a, ctrl-k

    options:list - list of choices for tab completion
    """

    # Clean out the options
    options = [o.strip() + " " for o in options] if options else []

    # Create the completer using the options
    def complete(text, state):
        results = [x for x in options if x.startswith(text)] + [None]
        return results[state]
    readline.set_completer(complete)

    # Insert the default when we launch
    def start():
        readline.insert_text(default)
    readline.set_startup_hook(start)

    # Actually perform the input
    try:
        value = input(prompt)
    finally:
        readline.set_startup_hook()
        readline.set_completer(null_complete)
    return value.strip()

def tryit():
    """Quick and dirty tester function"""
    return rlinput(prompt='>', default='delete me', \
            options=['start','stop'])
