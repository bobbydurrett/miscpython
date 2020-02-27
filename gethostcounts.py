# read through listener.log
# get count of hosts from incoming connections
# this is from an 11.2.0.4 listener log on HP Unix

# keep track of how many times each host appears

host_counts = dict()

print("reading file")

with open('listener.log') as f:
    for line in f:
        if 'HOST=' in line:
            first_host = line.find('HOST=')
            partial_line = line[first_host+5:]
            second_host = partial_line.find('HOST=')
            partial_line2 = partial_line[second_host+5:]
            parenthesis = partial_line2.find('(')
            incoming_host = partial_line2[:parenthesis-1]
            if incoming_host not in host_counts:
                host_counts[incoming_host] = 1
            else:
                host_counts[incoming_host] += 1

"""

sort by values - counts
https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value

>>> h = dict()
>>> h[3]='sfa'
>>> h[2]='fff'
>>> h
{3: 'sfa', 2: 'fff'}
>>> sorted(h.items(),key=lambda kv: kv[1])
[(2, 'fff'), (3, 'sfa')]
>>> sorted(h.items(),key=lambda kv: kv[1],reverse=True)
[(3, 'sfa'), (2, 'fff')]

"""

print("sorting list")

sorted_hosts_counts = sorted(host_counts.items(),key=lambda kv: kv[1],reverse=True)

# get host names from ip addresses

import socket

print("looking up hostnames and printing in sorted order")

for host_count in sorted_hosts_counts:
    ip_address = host_count[0]
    num_connections = host_count[1]
    try:
        retval = socket.gethostbyaddr(ip_address)
        hostname = retval[0]
    except:
        hostname = ip_address
        
    print(hostname+" = "+str(num_connections))
    

             


