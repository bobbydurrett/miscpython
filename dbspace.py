"""

Get size and number of non-system objects in an
Oracle database.

"""

import cx_Oracle
import sys

def get_db_space(tns_name,username,password):
    """
    This function returns the size of the database in
    gigabytes and the number of non-system objects.
    
    Returned:
    
    size - in gigabytes
    num_objects - number of objects
    error string - error if returned
    
    """

    connect_string = username+"/"+password+"@"+tns_name
    
    # handle cx_Oracle.DatabaseError: ORA-03134: Connections to this server version are no longer supported.
    
    try:
        con = cx_Oracle.connect(connect_string)
    except cx_Oracle.DatabaseError as e:
        return None,None,str(e.args[0])
        
    cur = con.cursor()
    
    # get total physical space
    
    space_query = """
select sum(bytes)/(1024*1024*1024) Gigabytes from
(select bytes from dba_data_files
union all
select bytes from dba_temp_files
union all
select bytes from v$log)
    """

    cur.execute(space_query)
    
    size_gb = cur.fetchone()[0]
        
    # get number of non-system objects
    
    objnum_query ="""
select count(*)
from dba_objects
where owner not in 
(
'SYS',
'PUBLIC',
'XDB',
'SYSTEM',
'CTXSYS',
'GSMADMIN_INTERNAL',
'OJVMSYS',
'OUTLN',
'ORACLE_OCM',
'APPQOSSYS'
)
    """
    
    cur.execute(objnum_query)
        
    num_objects = cur.fetchone()[0]

    cur.close()
    con.close()
    
    return size_gb,num_objects,None
