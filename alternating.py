"""

takes in lines and splits into alternating ones.

one 
two
three
four

comes out

one
three

two 
four

"""

evenlines = []

odd = True

while True:
    try:
        line = input()
        if odd:
            print(line)
            odd = False
        else:
            evenlines.append(line)
            odd = True       
    except EOFError:
        break
        
print(" ")
for line in evenlines:
    print(line)
