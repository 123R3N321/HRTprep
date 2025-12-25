'''
Now, this is very hypothetical GUESS on what
HRT might have tested other candidates
in the onsite
'''
import heapq

'''
warm-up:
python does not support max heap natively, it can be simply
made by wrapping the heapq, which is min heap:
'''
class MaxHeap:
    import heapq
    def __init__(self,lst = None):
        if lst is not None:
            flip = [-i for i in lst]    #find all neg
            heapq.heapify(flip)
            self.heap = flip    # a min heap of a  neg --> max heap of pos

    def push(self,num):
        heapq.heappush(self.heap,-num)

    def pop(self):
        return -heapq.heappop(self.heap)

'''
BUT, that is not very interesting for
an interview, especially for something
more academia-flavor such as HRT;
a good question would be, "so how does heap
work UNDER THE HOOD?"
'''

#helper method of log(n-i) for heap invariant
def _siftDown(lst,i,n):
    while True:
        l = 2*i+1
        if l>=n: return # index overreach, we can stop
        nextI = l   #let's assume l index points at the next target
        r = l+1
        if r<n and lst[r]>lst[l]:   # ... but the r index might be a better target
            nextI = r
        if lst[i]>=lst[nextI]: return   # no swap is needed, we can stop entire algo
        lst[i], lst[nextI] = lst[nextI], lst[i] # swap
        i = nextI  #move on to next ind, note ind is bumped 2x at a time, allowing log(n-i) runtime

#now, just to show-off (also because while True is frowned upon)
def _recurSiftDown(lst,i,n):
    if 2*i+1>=n: return
    l = 2*i+1
    nextI = l   #at this point all operations safe

    r = l+1
    if r<n and lst[r]>lst[l]:
        nextI = r
    if lst[i]>=lst[nextI]: return # same sanity check as above
    lst[i], lst[nextI] = lst[nextI], lst[i]
    _recurSiftDown(lst,nextI,n)

'''
with the helper defined, we can support heapify, heappush, heappop
'''

'''
support heapq behavior of in-place modify
'''
def maxHeapify(lst):
    n = len(lst)
    # reverse heapify is stable
    for i in range(n//2-1,-1,-1):    #invariant: l = 2*ind+1 = 2* (len(lst)//2-1)+1 guaranteed in bound
        _siftDown(lst,i,n)

'''
surprisingly simple approach:
swap the top and bottom elem in the heap, 
simply pop() that bottom to retrieve the max,
and fix the branch starting from the top.
we done.
'''
def maxHeapPop(lst):
    n = len(lst)
    if n==0: raise Exception('empty heap!')
    if n==1: return lst.pop()

    lst[0],lst[-1] = lst[-1],lst[0]
    res = lst.pop()
    n-=1    #remember, we have one fewer elem now
    _siftDown(lst,0,n)  # we only need to fix one branch; no need for maxHeapify call! IMPORTANT!
    return res

'''
this is slightly tricky:
we need to sift up.
Note that sift up is
important for future uses,
but for now, we don have to 
separately define a _siftDown helper...
...more on this later.
'''
def maxHeapPush(lst,num):
    lst.append(num)
    n = len(lst)
    if n==1: return

    i = n-1
    while i>0:
        nextI = (i-1)//2    #invariant: make sure 2*nextI+1=i and 2*nextI+2=i; simple test with i=1 (nextI=0)
        if lst[nextI]>=lst[i]: return
        lst[i], lst[nextI] = lst[nextI], lst[i]
        i = nextI

'''
with the complete suite of heapify, push, and pop,
we can use our customized heap for real puzzles.

problem statement:
implement median heap: good for tacking running median
we need const time getter for median; logn time 
modification of the structure (insert, delete)
'''

class MedianHeap:
    # import heapq
    def __init__(self,lst = None):
        """
        arbitrary invariant: minHeap can have +1 elem than maxHeap,
        consider MedianHeap//2: left half is smaller than right half by 1
        """
        self.minHeap = []   # this is the med--hi heap: top is the med (can be +1) (top heap)
        self.maxHeap = []   # this is the lo--med heap: top is the med             (bot heap)
        if lst is not None:
            for each in lst:
                self.push(each) #just call the push method to handle it

    def push(self,num):
        if len(self.maxHeap)<len(self.minHeap): #only push into the lower heap when strictly less
            maxHeapPush(self.maxHeap,num)
        else:
            heapq.heappush(self.minHeap,num)

    def median(self):
        if len(self.maxHeap)==len(self.minHeap):
            return (self.minHeap[0]+self.maxHeap[0])/2
        if len(self.maxHeap)<len(self.minHeap):
            return self.minHeap[0]
        else:
            return self.maxHeap[0]

    #note pop is undefined as it is kinda ambiguous: do we want pop of the max or the min?


'''
next, when we might need siftUp helper?
supposed we have a change in priority level 
up, then we need it.
'''

def _siftUp(lst,i,n):
    if n==0: return
    while i>0:
        nextI = (i-1)//2
        if lst[nextI] >= lst[i]: return
        lst[i], lst[nextI] = lst[nextI], lst[i]
        i = nextI

'''
allows us to update a value at an ind pos
a bit of a silly example because
a big part of using heap is to treat
everything other than the top elem
as black-box; we shouldn't care
to modify an element at some ind pos.

you can also see this update func
can be easily modified and applied onto minheap
'''
def maxHeapUpdate(lst, ind, newVal):
    n = len(lst)
    if n<=ind: raise Exception('index out of range')
    origVal = lst[ind]
    lst[ind] = newVal
    if newVal>origVal:  #this value is getting bigger
        _siftUp(lst,ind,n)
    elif newVal<origVal:
        _siftDown(lst,ind,n)