"""

Read in tnsnames.ora file and parse it into a list
of lists where each list is one tnsnames.ora entry.

Should include:

tns entry name
host name
port number
service/sid 
service or sid name

i.e.

['ORCL.WORLD','localhost',1521,'SERVICE_NAME','ORCL']

or

['ORCL.WORLD','localhost',1521,'SID','ORCL']

"""

def read_file(file_name):
    """
    Reads all of the lines of a file in and removes newlines.
    Returns a list of strings which are the lines of the file.
    """

    with open(file_name) as f:
        all_lines = f.readlines()
    f.closed
    
    stripped_lines = []
    
    for line in all_lines:
        stripped_lines.append(line.rstrip())
    
    return stripped_lines
    
def remove_comments_blanklines(stripped_lines):
    """
    Takes a list of strings and removes the lines
    that are comments or blank lines
    """
    
    ret_lines = []
    
    for sline in stripped_lines:
        if len(sline) < 1:
            continue
        elif sline[0] != '#':
            ret_lines.append(sline)
            
    return ret_lines
    
def get_tns_entries(tns_lines):
    """
    Break into individual tns entries
    will return a list of lists of lines (strings)
    
    Assumes that the input is a list of strings 
    which are lines from a tnsnames.ora file with
    blank lines and comment lines removed.
    
    Returns a list of lists of lines (strings).
    Each list of lines is one tns entry.
    
    """
    
    # List of tns entries to be returned
    
    list_of_entries = []
    
    # current tns entry's list of lines
    
    curr_entry = None
    
    for input_line in tns_lines:
        if len(input_line) > 0:
            if input_line[0] != ' ' and \
                input_line[0] != '\t' and \
                input_line[0] != '(' and \
                input_line[0] != ')':
                # new tns entry
                if curr_entry != None:
                    # save previous entry on main list
                    list_of_entries.append(curr_entry)
                # start new entry
                curr_entry = [input_line]
            else:
                # another line in current entry
                curr_entry.append(input_line)
               
    if curr_entry != None:
        # save last entry on main list
        list_of_entries.append(curr_entry)
       
    return list_of_entries
    
def parse_tns_entry(entry):
    """
    Convert list of string version of tns entries
    into list with the needed value like
    ['ORCL.WORLD','localhost',1521,'SERVICE_NAME','ORCL']
    or 
    ['ORCL.WORLD','localhost',1521,'SID','ORCL']
    """
    
    # First line should be tns entry such as
    # ORCL.WORLD =
    # look for " ="
    index = entry[0].find(" =")
    if index > 1:
        entry_name = entry[0][0:index]
    
    # next look for everything else
    
    for line in entry:
        upper_line = line.upper()
        if "HOST" in upper_line:
            index = upper_line.find("HOST = ")
            # remove everything before HOST = 
            trimmed_line = upper_line[index+7:]
            # host name is everything before )
            index = trimmed_line.find(")")
            host_name = trimmed_line[0:index]
        if "PORT" in upper_line:
            index = upper_line.find("PORT = ")
            # remove everything before PORT = 
            trimmed_line = upper_line[index+7:]
            # port number is everything before )
            index = trimmed_line.find(")")
            port_number = int(trimmed_line[0:index])
        if "SERVICE_NAME" in upper_line:
            index = upper_line.find("SERVICE_NAME = ")
            # remove everything before SERVICE_NAME =  
            trimmed_line = upper_line[index+15:]
            # service name is everything before )
            index = trimmed_line.find(")")
            db_identifier = trimmed_line[0:index]
            service_sid = "SERVICE_NAME"
        if "SID" in upper_line:
            index = upper_line.find("SID = ")
            # remove everything before SID =  
            trimmed_line = upper_line[index+6:]
            # SID is everything before )
            index = trimmed_line.find(")")
            db_identifier = trimmed_line[0:index]
            service_sid = "SID"
            
    return [entry_name,host_name,port_number,service_sid,db_identifier]
    
def parse_tns_file(file_name):
    """
    Reads a tnsnames.ora file and returns a list of lists in this form:
    
    ['ORCL.WORLD','localhost',1521,'SERVICE_NAME','ORCL']
    or 
    ['ORCL.WORLD','localhost',1521,'SID','ORCL']
    
    """
    
    # read all of the lines from a tnsnames.ora file
    
    tns_lines1 = read_file(file_name)

    # get rid of comments and blank lines

    tns_lines2 = remove_comments_blanklines(tns_lines1)

    # break into individual tns entries
    # will return a list of lists of lines (strings)

    tns_entries = get_tns_entries(tns_lines2)

    # convert list of string version of tns entries
    # into list with the needed values
    # ['ORCL.WORLD','localhost',1521,'SERVICE_NAME','ORCL']
    # or ['ORCL.WORLD','localhost',1521,'SID','ORCL']

    output_list = []

    for entry in tns_entries:
        output_entry = parse_tns_entry(entry)
        output_list.append(output_entry)
    
    return output_list
    

    





