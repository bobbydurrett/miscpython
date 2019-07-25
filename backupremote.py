"""

Routines to backup a remote directory using sftp.
Backs up all the files in the full directory tree.

Assumes that the remote system is Linux/Unix and
the local system is Windows

"""

# Global variables within this module

hostname = None
port = None
username = None
password = None
start_directory = None
backup_dir = None
transport = None
sftp = None

import paramiko
import os
import datetime
import shutil
import sys
import stat
import os.path
        
def connect_to_sftp_server():    
    """

    Make sftp connection.
    Return transport and sftp handles.

    """  
    
    global transport
    global sftp
    
    # try twice
    
    try:
        transport = paramiko.Transport((hostname, port))
        transport.connect(username = username, password = password)
        sftp = paramiko.SFTPClient.from_transport(transport)
    except:
        print('Exception in connect_to_sftp_server')
        disconnect_from_sftp_server()
        transport = paramiko.Transport((hostname, port))
        transport.connect(username = username, password = password)
        sftp = paramiko.SFTPClient.from_transport(transport)        
    
def disconnect_from_sftp_server():    
    """

    Close sftp connection and transport.
    
    Ignore errors.

    """  
    
    global sftp
    global transport

    try:
        sftp.close()
    except:
        pass

    try:
        transport.close()
    except:
        pass

        
def get_subdirectories(remote_dir):
    """
    
    Returns a list of the subdirectories of remote_dir.
    
    """
    
    sftp.chdir(remote_dir)

    file_list = sftp.listdir_attr('.')
        
    subdirectories = []
    
    for one_file in file_list:
            if stat.S_ISDIR(one_file.st_mode):
                subdirectory = remote_dir+one_file.filename+'/'
                subdirectories.append(subdirectory)
            
    return subdirectories

def traverse_directory(remote_dir, directory_tree):
    """
    
    Gets all the subdirectories of remote_dir and calls this
    function on each of them to get their subdirectories.
    
    Each call updates the dictionary directory_tree with entries
    like this:
    
    key - directory path of a remote directory
    value - list of directory paths for the remote directory's
    subdirectories.
    
    """
    
    # Get list of subdirectories
    # Try again on dropped connection

    try:
        subdirectories = get_subdirectories(remote_dir)
    except paramiko.ssh_exception.SSHException:
        print('SSHException calling get_subdirectories on '+remote_dir+' retrying.')
        disconnect_from_sftp_server()
        connect_to_sftp_server()
        subdirectories = get_subdirectories(remote_dir)
        
    # update dictionary with subdirectory list
      
    directory_tree[remote_dir] = subdirectories
    
    for subdirectory in subdirectories:
        # Recursively build dictionary for subdirectory
        
        traverse_directory(subdirectory, directory_tree)
        
def get_directory_tree(root_dir):
    """
    
    Returns a dictionary structure that includes the name of every directory
    in the tree rooted at root_dir.
    
    The structure returned is a dictionary whose key is a directory in the tree
    and whose value is a list of the subdirectories of the directory.
    
    This top level function is not recursive because it opens and closes the
    sftp connection but it will call a recursive function to traverse the tree
    and update the dictionary.
    
    """
    
    # create empty structure
    
    directory_tree = dict()
    
    # call recursive function to fill in tree
    
    traverse_directory(root_dir, directory_tree)
    
    return directory_tree
    
def convert_to_local_subdir(local_dir, remote_subdir):
    """
    
    Convert a Linux subdirectory name like /cgi-bin/ to
    
    C:\\mydirectory\\cgi-bin
    
    """
    
    with_backslashes = remote_subdir.replace('/','\\')
    
    return local_dir+with_backslashes
        
def build_subdirectories(local_dir, directory_list):
    """
    
    Take the list of Linux directories with / as the root and build out the subdirectories
    under local_dir.
    
    """
    
    for remote_subdir in directory_list:
        local_subdir = convert_to_local_subdir(local_dir, remote_subdir)
        os.makedirs(local_subdir, exist_ok=True)
        
def get_filenames(remote_dir):
    """
    
    Returns a list of the non-directory files in remote_dir.
    
    """
    
    sftp.chdir(remote_dir)

    file_list = sftp.listdir_attr('.')
        
    filenames = []
    
    for one_file in file_list:
            if not stat.S_ISDIR(one_file.st_mode):
                filenames.append(one_file.filename)
            
    return filenames
        
def copy_files_in_directory(top_local_directory,remote_directory):
    """
    
    Use sftp to copy all the files in the remote directory down to the
    equivalent local diretory under top_local_directory.
    
    """
    
    local_directory = convert_to_local_subdir(top_local_directory, remote_directory)
    
    print('Backing up files in directory '+remote_directory+' to '+local_directory)
 
    os.chdir(local_directory)
    sftp.chdir(remote_directory)

    files = get_filenames(remote_directory)

    for f in files:
        # check if file exists locally
        # already backed up
        if not os.path.isfile(f):
            print('Backing up '+f)
            try:
                sftp.get(f, f)
            except PermissionError:
                print('Skipping '+f+' due to permissions')
                
def backup_remote(phostname, pport, pusername, ppassword, pstart_directory, pbackup_dir):
    """
    Backs up all of the files in a remote directory to a local directory using sftp.
    Assumes the remote host is linux and local host is windows.
    
    phostname - remote host name
    pport - remote host sftp port
    pusername - remote host sftp user
    ppassword - remote host sftp password
    pstart_directory - top level remote host directory (i.e. /)
    pbackup_dir - local windows backup directory (i.e. C:\\backup)
    
    """

    global hostname
    global port
    global username
    global password
    global start_directory
    global backup_dir
    global transport
    global sftp
    
    hostname = phostname
    port = pport
    username = pusername
    password = ppassword
    start_directory = pstart_directory
    backup_dir = pbackup_dir
    
    # connect to sftp server
    
    connect_to_sftp_server()
    
    # Get remote directory tree as a dictionary
    
    print('Getting the names of the remote directories')
    
    remote_directory_tree = get_directory_tree(start_directory)
    
    directory_list = list(remote_directory_tree.keys())
    
    # backup directories under local backup_dir
    # throwback to standalone script
    
    local_dir = backup_dir
    
    print('Creating the local directories under '+local_dir)
    
    # build out local subdirectories
    
    build_subdirectories(local_dir, directory_list)
    
    print('Backing up each directory')
    
    for remote_dir in directory_list:
        try:
            copy_files_in_directory(local_dir,remote_dir)
        except paramiko.ssh_exception.SSHException:
            print('SSHException calling copy_files_in_directory - first exception')
            disconnect_from_sftp_server()
            connect_to_sftp_server()
            try:
                copy_files_in_directory(local_dir,remote_dir)
            except paramiko.ssh_exception.SSHException:
                print('SSHException calling copy_files_in_directory - second exception')
                disconnect_from_sftp_server()
                connect_to_sftp_server()
                try:
                    copy_files_in_directory(local_dir,remote_dir)
                except paramiko.ssh_exception.SSHException:
                    print('SSHException calling copy_files_in_directory - third exception')
                    disconnect_from_sftp_server()
                    connect_to_sftp_server() 
                    try:
                        copy_files_in_directory(local_dir,remote_dir)
                    except paramiko.ssh_exception.SSHException:
                        print('SSHException calling copy_files_in_directory - fourth exception - skipping directory')
                        disconnect_from_sftp_server()
                        connect_to_sftp_server() 
     
    # quit sftp connection
    
    disconnect_from_sftp_server()

