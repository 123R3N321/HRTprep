'''
today's study plan:
1. exploration of fast sqrt -->newton's method
2. asyncio exploration -->httpx
'''

'''
first, we need to derive tangential line formula
for a line with slope m to pass x1, y1:
    line is: y = mx+b
    and obvi: y1 = mx1+b
    so b = y1-mx1
    and thus y = mx+y1-mx1 is general formula for it
    which can be re-written as y = y1 + m(x-x1)

    and, when the line is tangential to a generic graph,
    we obviously have m = f'
    so: y = y1+f' * (x-x1) is generic tangential line formula
    note here f' has const value using x1 val as indep var

next, since with any graph that crosses 0, its tanget line
will corss zero at a x value better than the tangent line intercept
x value (as long as the tangent itself is not 0 -- that is easy to check)
we first find that x,0 point, then find the tangent line of original graph
at that x val, and repeat. Recurrence:
    given y = y1+y1' * (x-x1) = 0, we have x = x1- (y1/y1') is labelled as
    x2 (because this x val is at a point closer to our desired point)
    and now if we use x2 onto the original graph and just keep at our computation,
    we have successfully derived newton's method:
    x_k+1 = x_k-(y_k/y_k')

lastly, let's apply that to our desired question: what is sqrt(a)?
re-write as x^2-a = 0 where x is what we want, x = sqrt(a)
f' = 2x, and we obviously have invariant x_k+1 = x_k-((x_k^2-a)/(2x_k))
= x_k - (x_k/2 - a/2x_k) = x_k/2 + a/2x_k
we can start with any initial x_0 

'''


# look for sqrt with k iterations
def newtonianSqrt(a, k, x=1):
    for _ in range(k):
        x = x / 2 + a / (2 * x)
    return x


'''
now, this implies that we can build a newtonian solver 
that is very powerful and very general purpose:
we can do the shopping question from yesterday with this

given k, iterations, and args with descending power coeffs 
for polynomial to be solved, give approx result (only positive real root)
we also pass in optional argument for starting approx num
small syntactic clean up: horner's method representation of polynomial
(((ax+b)x+c)x+d)+...) = ax^n + bx^(n-1)+ ...
'''


def newtonianSolver(k, *args, x=1):
    # print(f"unpacking args: iterations {k}, and coeffs {args}, seed at {x}")
    deg = len(args) - 1
    argsPrime = [args[i] * (deg - i) for i in range(deg)]

    def hornerForm(x, coeffs):
        res = 0
        for each in coeffs:
            res = res * x + each
        return res

    for _ in range(k):
        f = hornerForm(x, args)
        df = hornerForm(x, argsPrime)
        if df == 0:
            raise ZeroDivisionError("at some point gradient is 0, abort!")
        x -= f / df
    return x


'''
now, with newtonian solver, we can tackle the gift shopping
problem in a very different way
again, given total price of 1 round r
we have w >= r+2r+3r+....
        = 0.5r(k)(k+1)
        0 = 0.5rk^2 + 0.5rk -w
'''


def solveOneRound(w, k, items):
    ct = 0
    for each in items:
        price = k * each
        if price > w:
            return ct
        ct += 1
        w -= price
    return ct


def buyGifts(w, items):
    import math
    r = sum(items)
    n = len(items)
    if not items or w < items[0]: return 0
    if w < r:
        return solveOneRound(w, 1, items)
    coeffs = [0.5 * r, 0.5 * r, -w]
    seed = w if r // n <= 1 else w // (r // n)
    k = math.floor(newtonianSolver(10, *coeffs, x=seed))
    # print(f"intermediate: we can buy {k} rounds")
    ct = k * len(items)  # bought k rounds each round len(items) items
    w -= (coeffs[0] * k ** 2 + coeffs[1] * k)
    ct += solveOneRound(w, k + 1, items)
    return ct


def dumb(w, items):
    ct = 0
    ind = 0
    mul = 1
    if not items: return 0
    while w > items[ind] * mul:
        ct += 1
        w -= items[ind] * mul
        ind += 1
        if ind == len(items):
            mul += 1
            ind = 0  # reset ind
    return ct


if __name__ == '__main__':
    a = 12
    k = 30
    x = 3
    res = newtonianSqrt(a, k)
    # print(f"newtonian sqrt of {a} with {k} iterations over seed {x} gives: {res}. Precise result is: {a**0.5}")
    # newtonianRes = newtonianSolver(k,1,0,-a,x=a if a>=1 else 1)
    # print(f"with generic newtonian solver for sqrt of {a}, we get {newtonianRes}")
    print("=============")

    w = 100
    items = [1, 3, 4, 2, 9, 0, 2]
    ct1 = buyGifts(w, items)
    ct2 = dumb(w, items)
    check = ct1 == ct2
    print(f"smart solution: {ct1}, dumb: {ct2}, are they good? {check}")

