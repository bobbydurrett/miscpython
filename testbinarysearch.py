import binarysearch

def getkey(item):
    return(item[0])
    
def getvalue(item):
    return(item[1])

print
print "empty list"

print binarysearch.search(getkey,getvalue,[],1)

print
print "one element list"
            
print binarysearch.search(getkey,getvalue,[[1,1]],0)
print binarysearch.search(getkey,getvalue,[[1,1]],1)
print binarysearch.search(getkey,getvalue,[[1,1]],2)

print
print "two element list"

print binarysearch.search(getkey,getvalue,[[1,1],[2,2]],0)
print binarysearch.search(getkey,getvalue,[[1,1],[2,2]],1)
print binarysearch.search(getkey,getvalue,[[1,1],[2,2]],1.5)
print binarysearch.search(getkey,getvalue,[[1,1],[2,2]],2)
print binarysearch.search(getkey,getvalue,[[1,1],[2,2]],3)

print
print "three element list"

print binarysearch.search(getkey,getvalue,[[1,1],[2,2],[3,3]],0)
print binarysearch.search(getkey,getvalue,[[1,1],[2,2],[3,3]],1)
print binarysearch.search(getkey,getvalue,[[1,1],[2,2],[3,3]],1.5)
print binarysearch.search(getkey,getvalue,[[1,1],[2,2],[3,3]],2)
print binarysearch.search(getkey,getvalue,[[1,1],[2,2],[3,3]],2.5)
print binarysearch.search(getkey,getvalue,[[1,1],[2,2],[3,3]],3)
print binarysearch.search(getkey,getvalue,[[1,1],[2,2],[3,3]],4)

print
print "million element list"

l=[]

for i in range(1000000):
   l.append([i,i])
   
print "length of l = "+str(len(l))
   
print binarysearch.search(getkey,getvalue,l,-456436)
print binarysearch.search(getkey,getvalue,l,456436)
print binarysearch.search(getkey,getvalue,l,1456436)
