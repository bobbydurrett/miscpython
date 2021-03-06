import sys
import subprocess

"""

A function that supports running processes simply.

"""

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
