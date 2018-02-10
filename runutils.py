import sys
import subprocess

"""

A couple of functions that support running processes simply.

"""

def onearg():

    """

    Returns the command line arguments as a single string.
    
    i.e. python test.py one two three
    
    returns the string "one two three"
    
    Assumes that there is no more than one space between arguments.
    
    Kind of a kluge to get the command line arguments as a string.

    """
    
    if len(sys.argv) < 2:
        return ""

    onearg = sys.argv[1]

    for word in sys.argv[2:]:
        onearg += " " + word
        
    return onearg
    
def runone(cmdline,stdin):
    """
    Arguments:

    cmdline - command line as a string (not a list)

    stdin - a string with newlines which will be stdin for cmdline

    returns

    (stdout,stderr) where these are strings with newlines.

    """ 
    
    cmdlinelist = cmdline.split()

    p = subprocess.Popen(cmdlinelist,stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    
    (stdoutbytes,stderrbytes) = p.communicate(stdin.encode('utf-8'))
    
    return (stdoutbytes.decode('utf-8'),stderrbytes.decode('utf-8'))
