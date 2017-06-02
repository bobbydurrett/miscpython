"""    
    This module implements bisection search.
    
    Three global variables affect the behavior of the 
    search.
    
    Variable max_iterations indicates the maximum number of times
    that you can go through the search loop.
    
    Variable iterations indicates how many times the search
    went through the loop.
    
    Variable round_digits defines to how many digits after the
    decimal point that the search function will round.

"""

max_iterations = 1000000
round_digits = 4
iterations = -1


def search(f,lo,hi,target):
    """ 
        This function returns the parameter value for function f that
        causes f to return target.
       
        Parameters lo and hi are the minimum and maximum possible 
        parameter values for f. 
       
        The value f(hi) must be >= target and f(lo) must be <= target.
       
        Function f takes a float as a parameter and returns a float.
        The parameters lo, hi, and target are floats.
       
    """
    
    global iterations
    
    # Verify that lo and hi bracket the answer
    
    assert f(hi) >= target and f(lo) <= target
    
    # Answer needs to be within this amount of
    # target.
    
    how_close = 10**(-round_digits-2)
        
    iterations = 0
    
    while True:
        
        # Track iterations to stop infinite loop
        
        iterations += 1
        assert iterations < max_iterations
        
        # Try midpoint between current values
        # of lo and hi.
        
        new_x = (lo + hi) / 2.0
        new_result = f(new_x)
        new_diff = new_result-target
        
        # If we are close enough then return
        # rounded result.
        
        if abs(new_diff) <= how_close:
            return round(new_x,round_digits)
            
        # Replace lo or hi with previous midpoint.
            
        if (new_diff) < 0:
            lo = new_x
        else:
            hi = new_x
            
 # Should not be able to get here.
   
    assert False

# Run test if module run standalone

if __name__ == "__main__":

    import math
    
    # simple test function meant to be 
    # passed into search.  Divides
    # by 10.0
    
    def test(x):
        return x/10.0
        
    # Find the value of x for which test(x)
    # returns 6.0
    # Should return 60.0 since test
    # just divides by 10.0
        
    print(search(test,0.0,100.0,6.0))
    
    print(iterations)
    
    print(search(math.sqrt,0.0,100.0,6.0))
    
    print(search(math.exp,0.0,100.0,6.0))
    
    round_digits = 8
    
    print(search(math.log,0.1,1000.0,6.0))
    
