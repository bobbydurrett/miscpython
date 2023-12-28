"""

archivelogspace.py

for a given database with a given size of archive log filesystem output
an estimate of space used and percent used of the filesystem after each
archive log is written. assumes we have backups at fixed times every day
which keep a fixed number of hours of archive log history.

pseudo code

get archivelog filesystem size in bytes

get backup times (hours,minutes,seconds) and hours of retention
assuming same backup times every day. 

get username password and tnsname for database

read in size in bytes, write time, and name for all archivelogs

set bytes used in filesystem to 0
set last archive log time to 1/1/1900
set list of archive logs on disk to empty list

loop through all archivlogs in order of write time starting with oldest.

    if backup time occurs between last archive log time and current archive log time:
       remove all archive logs from list that are older than retention time and
       subtract their size from bytes used in filesystem
       
    add archivelog size to bytes used in filesytem
    
    output bytes used in filesystem and percent used and date and time and archivelog name
    
    add archivelog to list of archivelogs on disk
"""

import cx_Oracle
from datetime import datetime, time, timedelta
from sys import argv, exit

"""

Functions

"""

def get_log_info(username,password,tnsname):
    """
    Return list of archive logs in order by time they were
    written and sequence number.
    """

    query = """
select 
(BLOCKS+1)*BLOCK_SIZE,
COMPLETION_TIME,
NAME file_name
from 
V$ARCHIVED_LOG
order by
COMPLETION_TIME,
SEQUENCE#
"""

    connect_string = username+'/'+password+'@'+tnsname
    con = cx_Oracle.connect(connect_string)
    cur = con.cursor()
    
    cur.execute(query)
    
    log_info = []
           
    for result in cur:
        log_info.append(result)
    
    cur.close()
    con.close()
    
    return log_info
    
def get_backup_dateetime(last_log_time,curr_log_dttime,backup_time):
    """
    
    Get date and time of backup that runs at the given time and is between
    the last log date and time and the current log date and time.
    
    backup_time is just a time of day like 4 am
    
    return None if none found
    
    our assumption is that curr_log_dttime >= last_log_time
    but they could be the same day or several days apart.
    
    so I think we need to start with the day of curr_log_dttime and loop
    backwards 24 hours at a time trying the backup time for each day to see 
    if it is between last_log_time and curr_log_dttime
    
    if there are multiple days between the two logs pick the last one because
    with the retention it will remove the most logs
    
    """
    
    last_backup_datetime = datetime.combine(curr_log_dttime.date(),backup_time)
    first_backup_datetime = datetime.combine(last_log_time.date(),backup_time)
    day_interval = timedelta(days=1)
    
    backup_datetime = last_backup_datetime
    
    while backup_datetime >= first_backup_datetime:
        if backup_datetime > last_log_time and backup_datetime < curr_log_dttime:
            return backup_datetime
        backup_datetime -= day_interval
    
    return None
    
def check_for_backup(last_log_time,curr_log_dttime,backup_times):
    """
    See if any of the backup times occur between the prev and
    current logs
    
    """
    
    for bkp in backup_times:
        backup_time = bkp[0]
        retention = bkp[1]
        # get backup date and time that is between the last and current log datetimes
        backup_datetime = get_backup_dateetime(last_log_time,curr_log_dttime,backup_time)
        # return if found
        if backup_datetime != None:
            return backup_datetime,retention

    return None, None
    
def remove_old_logs(backup_datetime,retention,logs_on_disk,bytes_used):
    """
    remove logs from disk based on backup retention
    """
    # remove logs from logs_on_disk list
    # that exceed the backup retention
    new_logs = []
    
    for log in logs_on_disk:
        # date and time of current log on disk being checked
        log_ddtime = log[1]
        # first condition checks time is > backup time
        # second condition checks if datetime > previous log
        # for log datetime + retention
        if (log_ddtime + retention) > backup_datetime:
            new_logs.append(log)
        else:
            size_bytes = log[0]
            bytes_used -= size_bytes
            
    logs_on_disk = new_logs    

    return logs_on_disk,bytes_used
    
def print_info(item,bytes_used,filesystem_size):
    """
    print information for one archive log file
    """
 
    if item[2] == None:
        log_name = " "
    else:
        log_name = item[2]
        
    percent_used = round((100*bytes_used)/filesystem_size,2)
    
    log_size_bytes = item[0]
    
    datetime_written = str(item[1])
      
    print(datetime_written+' '+str(percent_used)+'% '+log_name)
            
def process_one_log(item,bytes_used,last_log_time,logs_on_disk,backup_times,filesystem_size):
    """
    Logic for just one log in the list
    item is the log entry like
    
    (24576, datetime.datetime(2023, 12, 12, 3, 30, 29), '/myfs/MYDB/archive/MYDB1150995676_1_113.arc')
    
    """

    # if backup time occurs between last archive log time and current archive log time:
    # remove all archive logs from list that are older than retention time and
    # subtract their size from bytes used in filesystem

    # date and time current log was written
    curr_log_dttime = item[1]
    
    # Check for backup time between the previous and current logs
    
    backup_datetime,retention = check_for_backup(last_log_time,curr_log_dttime,backup_times)
    
    # Remove logs that backup would remove based on retention

    if backup_datetime != None:
    
        logs_on_disk,bytes_used = remove_old_logs(backup_datetime,retention,logs_on_disk,bytes_used)
                
    # add archivelog size to bytes used in filesytem
    
    bytes_used += item[0]

    # add archivelog to list of archivelogs on disk
    
    logs_on_disk.append(item)
    
    # set last log time to current
    
    last_log_time = curr_log_dttime
    
    # output bytes used in filesystem and percent used and date and time and archivelog name

    print_info(item,bytes_used,filesystem_size)

    return bytes_used,last_log_time,logs_on_disk
    
def process_log_info(log_info,filesystem_size,backup_times):
    """
    Main loop
    """
    # set bytes used in filesystem to 0
    
    bytes_used = 0
    
    # set last archive log time to 1/1/1900 midnight
    
    last_log_time = datetime(1900,1,1,0,0,0)
    
    # set list of archive logs on disk to empty list
    
    logs_on_disk = []
    
    # keep track of max percent and date
    
    max_percent_used = 0
    max_date = last_log_time
    
    # loop through all archivlogs in order of write time starting with oldest.
    
    for item in log_info:
    
        bytes_used,last_log_time,logs_on_disk = process_one_log(item,bytes_used,last_log_time,logs_on_disk,backup_times,filesystem_size)
        
        pct_used = (100*bytes_used)/filesystem_size
        
        if pct_used > max_percent_used:
            max_percent_used = pct_used
            max_date = last_log_time
                
    return max_percent_used,max_date
    


def read_file(filename):
    """
    Read in file in this format:

    archivelog filesystem size in bytes
    number of backups per day
    one line per backup with 24-hour:minutes:seconds archivlog-retention-hours

    """
    
    with open(filename, encoding="utf-8") as f:
        lines = f.read().split('\n')
        
        filesystem_size = int(lines[0])
        
        num_backups = int(lines[1])
        
        backup_times = []
        
        for i in range(num_backups):
            backup_line = lines[i+2]
            hour = int(backup_line[0:2])
            minute = int(backup_line[3:5])
            second = int(backup_line[6:8])
            backup_time=time(hour,minute,second)
            retention_hours = timedelta(hours=int(backup_line[9:]))
            backup = [backup_time,retention_hours]
            backup_times.append(backup)

    return filesystem_size,backup_times

    
"""

Main program

"""

# Get global variables

if len(argv) != 5:
    print("""
Arguments: oracle-username oracle-password tns-name configfile-name

Config file is text file with this format:

archivelog filesystem size in bytes
number of backups per day
one line per backup with 24-hour:minutes:seconds archivlog-retention-hours

for example:

8795958804480
6
02:15:00 168
06:15:00 168
10:45:00 168
14:15:00 168
18:15:00 168
22:15:00 168
    """)
    exit()
    
# filename

filename = argv[4]

filesystem_size,backup_times = read_file(filename)

# username password and tnsname for database

username = argv[1]
password = argv[2]
tnsname = argv[3]

# read in size in bytes, write time, and name for all archivelogs

log_info = get_log_info(username,password,tnsname)

# do the main loop printing the space used in the filesystem after
# each archive log is added

max_percent_used,max_date = process_log_info(log_info,filesystem_size,backup_times)

print(' ')
print('Max percent used archivelog filesystem: '+str(round(max_percent_used,2))+'%')
print('Date and time of max percent: '+str(max_date))


