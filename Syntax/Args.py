'''
triangular inequality question extended:

given any number of arrays A, B, C, ...
they only contain integers.
we want to find the minimal value of d, where
d = |a-b|+|b-c|+|a-c|+....
where a, b, c, ... are arbitrary elements from
the arrays A, B, C... respectively.

Mathematically, we can also regard a, b, c, ... as
the sides of a n-polygon where n is the number of arrays we have
and each array A, B, C ... contains all possible length of the
corresponding side, and d is the sum of the differences between
all pairs of sides, taking the absolute value.

Find the minimal such d.

'''
def foo(*args):
    for each in args:
        print(each)

def argsComp(*args):
    n = len(args)   #how many arrays we have
    bumpers = [0]*n

    for i in range(n):
        args[i].sort()

    d = float('inf')
    while condition(bumpers, *args):
        lst = [args[i][bumpers[i]]  if bumpers[i]<len(args[i]) else float('inf') for i in range(n)]  #take all sides
        print(f"lst is {lst}")
        d = min(d, compute(lst))
        if d==0: return d
        inced = findMin(lst)
        bumpers[inced]+=1
    return d

'''
helper func to compute the polygonal side min dif
'''
def compute(lst):
    res = 0
    for i in range(len(lst)):
        for j in range(i+1,len(lst)):
            res+=abs(lst[i]-lst[j])
    return res

def findMin(lst):
    smallest = lst[0]
    resI = 0
    for i, val in enumerate(lst):
        if val<smallest:
            resI=i
    return resI

def condition(bumpers, *args):
    check = False
    for bp,collec in zip(bumpers, args):
        check = check or bp<len(collec)
    return check



if __name__ == "__main__":
    A = [1,2,3,4,5]
    B = [2,3,4,5,6]
    C = [7,9,11,37,19]
    res = argsComp(A,B,C)
    print(f"result of comparing arrays is {res}")