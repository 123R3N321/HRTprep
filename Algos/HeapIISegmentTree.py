'''
my attempt at segment tree
'''


class Node:
    def __init__(self, val, l=None, r=None):
        self.left = l
        self.right = r
        self.val = val  # stores tuple of segment max, l, r


def printTree(root, indent=0):
    if root:
        printTree(root.right, indent + 8)

        print('\n' + ' ' * indent + f"{root.val}")
        printTree(root.left, indent + 8)


def buildSegMax(arr, l, r):
    if r <= l + 1:
        return Node((arr[l], l, r))  # val -- l -- r  tuple

    mid = (l + r) // 2
    left = buildSegMax(arr, l, mid)
    right = buildSegMax(arr, mid, r)
    localVal = (max(left.val[0], right.val[0]), l, r)
    return Node(localVal, left, right)


'''
abstract tree build (not actual tree)

'''

'''
abstract tree build (not actual tree)

'''


def buildAbstractSegMax(arr, l, r):
    n = r - l
    m = 1
    while m < n:
        m <<= 1  # we want least power of 2 that contains n
    res = [float('-inf')] * (m * 2 - 1)
    leafStart = m - 1
    for i in range(n):
        res[leafStart + i] = arr[l + i]
    for j in range(leafStart - 1, -1, -1):
        res[j] = max(res[2 * j + 1], res[2 * j + 2])
    return res, leafStart


def printHeap(arr, i=0, indent=0):
    if i < len(arr):
        printHeap(arr, 2 * i + 2, indent + 4)
        val = f"{arr[i]}({i})" if arr[i] > float('-inf') else f'_({i})'
        print(' ' * indent + val)
        printHeap(arr, 2 * i + 1, indent + 4)


'''
locate the index pos of the correct basket
'''


def findBasket(tree, elem, leafStart):
    if tree[0] < elem:
        return -1  # the moment this happens we know no search needed; conversely if this does not happen we always have a basket that is good
    i = 0
    while i < leafStart:
        l = 2 * i + 1
        if tree[l] >= elem:
            i = l
        else:
            i = l + 1
    return i


'''
given the index of the basket to be occupied,
fill it.
'''


def fillBasket(heap, i):
    heap[i] = float('-inf')  # fill the basket
    while i > 0:
        parentI = (i - 1) // 2  # parent ind pos
        print(f"updating index {parentI}")
        newVal = max(heap[2 * parentI + 1], heap[2 * parentI + 2])
        if heap[parentI] == newVal: break
        heap[parentI] = newVal
        # braindead update. Lotta ways to improve it.
        i = parentI
        print(f"updated to be val {heap[parentI]}")
    return heap[0]  # finally we check what is the overall max after update


def driver(fruits, baskets):
    segMaxHeap, leafStart = buildAbstractSegMax(baskets, 0, len(baskets))
    ct = len(fruits)
    check = segMaxHeap[0]
    for each in fruits:
        basketInd = findBasket(segMaxHeap, each, leafStart)  # find the earliest fit
        if basketInd > -1:
            ct -= 1  # found a good basket

            print(
                f"currently checking fruit of size {each}, and found earliest basktet at ind {basketInd} with size {segMaxHeap[basketInd]}.")

            check = fillBasket(segMaxHeap, basketInd)  # fill it, update tree branch
            print(f"After occupying it, the biggest basket has size {check}, we have {ct} remaining fruits.")
    return ct


if __name__ == '__main__':
    arr = [1, 4, 2, 3, 6, 9, 5, 2, 0]
    root = buildSegMax(arr, 0, len(arr))
    # printTree(root)
    arr = [4, 7, 8]
    heap = buildAbstractSegMax(arr, 0, len(arr))
    printHeap(heap)
    # fruits = [4,1,3,2,5]
    # baskets = [1,9,3,2,1]
    # fruits = [6,5]
    # baskets = [3,5]
    fruits = [7, 5, 8]
    baskets = [4, 7, 8]
    print(driver(fruits, baskets))
