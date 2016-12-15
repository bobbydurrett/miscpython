import math
import bisection

help(bisection)

# simple test function meant to be 
# passed into search.  Divides
# by 10.0

def test(x):
    return x/10.0
    
# Find the value of x for which test(x)
# returns 6.0
# Should return 60.0 since test
# just divides by 10.0
    
print bisection.search(test,0.0,100.0,6.0)

print bisection.iterations

print bisection.search(math.sqrt,0.0,100.0,6.0)

print bisection.search(math.exp,0.0,100.0,6.0)

bisection.round_digits = 8

print bisection.search(math.log,0.1,1000.0,6.0)