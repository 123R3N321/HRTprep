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


def buildAbstractSegMax(arr, l, r):
    n = r - l
    m = 1
    while m < n:
        m <<= 1  # we want least power of 2 that contains n
    res = [float('-inf')] * (m * 2 - 1)
    for i in range(n):
        res[m - 1 + i] = arr[l + i]
    for j in range(m - 1 - 1, -1, -1):
        res[j] = max(res[2 * j + 1], res[2 * j + 2])
    return res


if __name__ == '__main__':
    arr = [1, 4, 2, 3, 6, 9, 5, 2, 0]
    root = buildSegMax(arr, 0, len(arr))
    printTree(root)