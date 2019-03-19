"""

Get database version.
Works with Oracle databases.

"""

import cx_Oracle
import sys

def get_db_version(tns_name,username,password):
    """
    The main purpose of this function is to return the version
    of an oracle database such as 11.2.0.4. 
    
    It also returns other helpful information to verify that you
    are connected to the correct database.
    
    Returned:
    
    version - VERSION from v$instance with trailing .0 removed
    instance name - INSTANCE_NAME from v$instance
    host name - HOST_NAME from v$instance
    db name - NAME from v$database
    error string - error if returned
    
    """

    connect_string = username+"/"+password+"@"+tns_name
    
    # handle cx_Oracle.DatabaseError: ORA-03134: Connections to this server version are no longer supported.
    
    try:
        con = cx_Oracle.connect(connect_string)
    except cx_Oracle.DatabaseError as e:
        return None,None,None,None,str(e.args[0])
        
    cur = con.cursor()
    
    # get columns from v$instance

    cur.execute("select VERSION,INSTANCE_NAME,HOST_NAME from V$INSTANCE")
    
    version,instance_name,host_name = cur.fetchone()
    
    # trim off trailing .0 from version
    
    if version[-2:] == '.0':
        version = version[:-2]
    
    # get column from v$database
    
    cur.execute("select NAME from V$DATABASE")
        
    db_name = cur.fetchone()[0]

    cur.close()
    con.close()
    
    return version,instance_name,host_name,db_name,None
