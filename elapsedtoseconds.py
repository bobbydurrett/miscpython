"""

Reads lines in this format from standard input:

Elapsed: 00:38:39.52

Outputs the equivalent number of seconds.

i.e. (38*60)+39.52 = 2319.52

So, in this case this script outputs 2319.52.

"""

while True:
    try:
        line = input()
        # get rid of "Elapsed: "
        timeonly = line[9:]
        # assume hours and minutes are two characters
        # separated by a colon
        hours = int(timeonly[0:2])
        minutes = int(timeonly[3:5])
        # seconds in rest
        seconds = float(timeonly[6:])
        print(str(hours*3600+minutes*60+seconds))
    except EOFError:
        break
        
        

    
