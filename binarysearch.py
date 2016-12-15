"""    
    This module implements binary search.
    
    It assumes that you have a list of items
    sorted by a key and that there is a value 
    for each item.
    
"""

def search(getkey,getvalue,sortedlist,targetkey):
    """ 
        This function returns the value for the
        list item with the key targetkey.
        
        getkey is a function that takes a list
        item and returns its key.
        
        getvalue is a function that takes a list
        item and returns its value.
        
        sortedlist is the list.
        
        targetkey is the key for the list item
        that you want to find.
       
    """
    
    lo = 0
    hi = len(sortedlist)-1
    
    if hi < 0:
        return None
    
    if getkey(sortedlist[lo]) > targetkey or getkey(sortedlist[hi]) < targetkey:
        return None   
    
    while hi > (lo+1):
        mid = (lo+hi)/2
 #       print "lo="+str(lo)
 #       print "hi="+str(hi)
 #       print "mid="+str(mid)
        
        assert getkey(sortedlist[mid]) >= getkey(sortedlist[lo])
        assert getkey(sortedlist[mid]) <= getkey(sortedlist[hi])
        
        if getkey(sortedlist[mid]) == targetkey:
            return getvalue(sortedlist[mid])
        elif getkey(sortedlist[mid]) > targetkey:
            hi = mid
        else:
            lo = mid

            
    if getkey(sortedlist[lo]) == targetkey:
            return getvalue(sortedlist[lo])
        
    if getkey(sortedlist[hi]) == targetkey:
            return getvalue(sortedlist[hi])
            
    return None
    
# Run test if module run standalone

if __name__ == "__main__":

    def getkey(item):
        return(item[0])
        
    def getvalue(item):
        return(item[1])
    
    print
    print "empty list"
    
    print search(getkey,getvalue,[],1)
    
    print
    print "one element list"
                
    print search(getkey,getvalue,[[1,1]],0)
    print search(getkey,getvalue,[[1,1]],1)
    print search(getkey,getvalue,[[1,1]],2)
    
    print
    print "two element list"
    
    print search(getkey,getvalue,[[1,1],[2,2]],0)
    print search(getkey,getvalue,[[1,1],[2,2]],1)
    print search(getkey,getvalue,[[1,1],[2,2]],1.5)
    print search(getkey,getvalue,[[1,1],[2,2]],2)
    print search(getkey,getvalue,[[1,1],[2,2]],3)
    
    print
    print "three element list"
    
    print search(getkey,getvalue,[[1,1],[2,2],[3,3]],0)
    print search(getkey,getvalue,[[1,1],[2,2],[3,3]],1)
    print search(getkey,getvalue,[[1,1],[2,2],[3,3]],1.5)
    print search(getkey,getvalue,[[1,1],[2,2],[3,3]],2)
    print search(getkey,getvalue,[[1,1],[2,2],[3,3]],2.5)
    print search(getkey,getvalue,[[1,1],[2,2],[3,3]],3)
    print search(getkey,getvalue,[[1,1],[2,2],[3,3]],4)
    
    print
    print "million element list"
    
    l=[]
    
    for i in range(1000000):
       l.append([i,i])
       
    print "length of l = "+str(len(l))
       
    print search(getkey,getvalue,l,-456436)
    print search(getkey,getvalue,l,456436)
    print search(getkey,getvalue,l,1456436)
