"""

Script to run a list of commands on a remote Unix or Linux server.

"""

import paramiko
import sys
import socket
import os

def create_shell_script(script_name,command_list):
    """
    
    Create the file script_name in the current directory
    and write the lines in command_list to it.
    These lines should be Unix or Linux shell script commands
    such as ls or pwd.
    
    """
    
    f = open(script_name, 'wb')
    
    for command in command_list:
        f.write((command+'\n').encode('utf-8'))
        
    f.close()
    
def upload_shell_script(script_name,host,username,password):
    """
    
    Copy script to remote host.
    
    """
    
    # connect to sftp server
    
    transport = paramiko.Transport((host, 22))
    transport.connect(username = username, password = password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    # copy to server
    
    sftp.put(script_name, script_name)
    
    # make executable
    
    sftp.chmod(script_name, 0o700)
    
    # close connection
    
    sftp.close()
    transport.close()
    
def strip_newlines(line_list):
    """
    
    Take a list of strings and return the same
    list with all of the newline characters 
    removed.
    
    """
    
    new_list=[]
    for line in line_list:
        new_list.append(line.strip('\n'))
        
    return new_list
    
def run_shell_script(script_name,host,user,pwd):
    """
    
    Run the named shell script on a remote host.
        
    """
    
    client = paramiko.SSHClient()
    
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
    
    client.connect(host,username=user, password=pwd)
    
    stdin, stdout, stderr = client.exec_command('./'+script_name)
    
    out=strip_newlines(stdout.readlines())  
    err=strip_newlines(stderr.readlines())
    
    return out,err
    
def delete_shell_script(script_name,host,username,password):
    """
    
    Delete the remote script.
    
    """
    
    # connect to sftp server
    
    transport = paramiko.Transport((host, 22))
    transport.connect(username = username, password = password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    # copy to server
    
    sftp.remove(script_name)
        
    # close connection
    
    sftp.close()
    transport.close()
    
def run_command_list(host,username,password,command_list):
    """
    
    Takes the name of a Unix or Linux host and scps command_list
    to the host as a script and runs it.
    
    For sudo to oracle this will work:
    
    sudo -S -p '' su - oracle << EOF
    MY PASSWORD
    commands here
    EOF
    
    """
    
    script_name='remote_script.sh'
    
    # create shell script as local file
    
    create_shell_script(script_name,command_list)
    
    # copy script to remote host
    
    upload_shell_script(script_name,host,username,password)
        
    # execute script on remote host
    
    out,err = run_shell_script(script_name,host,username,password)
    
    # remove remote script
    
    delete_shell_script(script_name,host,username,password)
    
    # remove local script
    
    os.remove(script_name)
    
    return out,err

def run_command_list_as_oracle(host,username,password,command_list):
    """
    
    Runs a list of Unix or Linux commands sudo'd to oracle.
    
    """
    oracle_command_list = ["sudo -S -p '' su - oracle << EOF", password]
    oracle_command_list += command_list + ["EOF"]
    
    return run_command_list(host,username,password,oracle_command_list)
    
def get_remote_file(directory_path,file_name,host,username,password):
    """
    
    Get a file from the remote host.
    
    Get from remote directory but save it in the current
    local directory.
    
    """
    
    # connect to sftp server
    
    transport = paramiko.Transport((host, 22))
    transport.connect(username = username, password = password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    # copy to server
    
    sftp.get(directory_path+'/'+file_name, file_name)
    
    # close connection
    
    sftp.close()
    transport.close()