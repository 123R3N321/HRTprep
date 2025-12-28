'''
I passed round one using bisect.
In hindsight, chatgpt gave a diff solution
that did not involve bisect
but still...
'''

'''
let's start with my own implementation of LC1351
note that, in worst case, this approach is no better than linear (when zigzag dominates)
a theoretical better solution will be to try to bisect the end of non-neg, after 
trying to bisect start of neg and realizing that start is first row

trick: for descending sorted collection, bisect_left(collection, -pivotVal, key=lambda x:-x)
we invert both the lambda and the pivot val. Same trick as maxheap wrapper.
'''
import bisect
def bisectCt(mat):
    n = len(mat)
    if n<=0: return 0
    m = len(mat[0])
    if m<=0: return 0
    ct = 0
    cut = bisect.bisect_left(mat,1,key=lambda x: -x[0])
    ct+= (n-cut)*m
    if cut<=0: return ct
    print(f"after big cut, cut at ind{cut}, ct is at {ct}")
    ct+=zigzag(mat,cut-1,m)
    return ct

def zigzag(mat,cut,m):
    ct=0
    mp = 0
    while cut>-1 and mat[cut][-1]<0:
        mp = bisect.bisect_left(mat[cut],1,key=lambda x: -x)
        print(f"each mp at cut: {cut} with ind in row {mp}")
        ct+=m-mp
        cut-=1
    return ct

if __name__ == "__main__":
    mat = [[4,3,2,-1],[3,2,1,-1],[1,1,-1,-2],[-1,-1,-2,-3]]
    for each in mat:
        print(each)
    print("------------")
    print(f"res: {bisectCt(mat)}")

