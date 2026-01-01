'''
ok, a very hardcore solution to the leetcode
1. transpose and define the problem as "water crosses sideways"
2. each water cell has a timestamp
3. binary scope the dfs
very complicated!
'''

'''
add-on comment:
ok Turns out my solution is too slow and the correct approach is UnionFind
Good! I haven't come across it in a while. Time to revisit.
But that is tomorrow's problem!

'''

def makeRoad(ro, co, cells):
    road = [[co * ro for _ in range(ro)] for __ in range(co)]
    # transpose!
    # values are day stamps of becoming water
    # initial value at co to indicate land: the water val has
    # invariant 0<=waterVal<co !
    for day, (r, c) in enumerate(cells):
        road[c - 1][r - 1] = day  # transposed populate!
    return road


'''
now we have a helper to create the road mat, 
we need another helper for dfs determine if water has connected
BFS is better
also we can compress space use to only O(ro size)
'''
from collections import deque


def dayBFS(road, day):
    end = len(road)
    rend = len(road[0])
    q = deque()
    ct = 0
    for i, each in enumerate(road[0]):
        if each <= day:
            q.append(i)
            ct += 1
    # initial setup complete
    r = 1  # we only need to check next ro
    while q:  # as long as q not empty
        if r >= end: return True
        added = set()
        nextCt = 0
        for _ in range(ct):  # we pop all from one level and explore next level
            i = q.popleft()
            for nextI in [i - 1, i, i + 1]:

                if 0 <= nextI < rend and road[r][nextI] <= day and nextI not in added:
                    nextCt += 1
                    q.append(nextI)
                    added.add(nextI)
        r += 1
        ct = nextCt
    return False


'''
turns out the bfs solution
is a misinterpretation of what
the qn wants
end = len(road)
single source dfs to be
called by each starting point on 1st row ind 0 row
pass in the coord as start
'''


def dayDFS(road, day, start, goal, seen):
    d, i = start
    if 0 <= d < len(road) and 0 <= i < len(road[0]) and (d, i) not in seen and road[d][i] <= day:
        if d >= goal:
            return True
        seen.add((d, i))
        n = dayDFS(road, day, (d - 1, i), goal, seen)  # north
        l = dayDFS(road, day, (d, i - 1), goal, seen)
        r = dayDFS(road, day, (d, i + 1), goal, seen)
        s = dayDFS(road, day, (d + 1, i), goal, seen)  # south
        sl = dayDFS(road, day, (d + 1, i - 1), goal, seen)
        sr = dayDFS(road, day, (d + 1, i + 1), goal, seen)
        nl = dayDFS(road, day, (d - 1, i - 1), goal, seen)
        nr = dayDFS(road, day, (d - 1, i + 1), goal, seen)
        return l or r or s or sl or sr or n or nl or nr
    else:  # out of bound, or repeat path, or simply future day
        return False


def dayDFSDriver(road, day):
    starts = [(0, i) for i, sday in enumerate(road[0]) if sday <= day]
    res = False
    seen = set()
    goal = len(road) - 1
    for each in starts:
        res = res or dayDFS(road, day, each, goal, seen)
        seen.clear()
    return res


'''
we have all the pieces we want. Last step is binary search
total 0--5
iteration       l   m   r
1               0   2   5

2               

'''


def binarySearch(road, n):
    l = 0
    r = n - 1  # actually much smaller than this
    while l <= r:  # smaller equal is ok
        mid = (l + r) // 2
        res = dayBFS(road, mid)
        if res:
            r = mid - 1
        else:
            l = mid + 1
    return l


def checkRoad(road, cells):
    print("obtained road:")
    # for eachRow in road:
    #     print(eachRow)
    print("=============")
    pool = []
    for i in range(len(road)):
        for j in range(len(road[0])):
            day = road[i][j]
            if day < len(road) * len(road[0]):
                pool.append((day, j, i))  # day - ro - col (restored transpose)
    pool = sorted(pool, key=lambda x: x[0])
    rcells = [[trip[1] + 1, trip[2] + 1] for trip in pool]
    # print(f'rcells is: {rcells}')
    print(f"check if restoration is good: {rcells == cells}")
    if rcells != cells:
        raise Exception("bad road")
    print("road: ")
    for eachRow in road:
        print(eachRow)


def checkRoadD(road, d):
    for eachRow in road:
        visual = [each if each <= d else '_' for each in eachRow]
        for each in visual:
            print(each, end='\t')
        print()


'''
for better visual
'''


def transpose(mat):
    n = len(mat)
    m = len(mat[0])
    resMat = [[None for _ in range(n)] for __ in range(m)]
    for i in range(n):
        for j in range(m):
            resMat[j][i] = mat[i][j]
    return resMat


###############fast solution: union find (this is copied from solutions section of leetcode)

from typing import List


class Solution:
    def latestDayToCross(self, row: int, col: int, cells: List[List[int]]) -> int:
        n = row * col
        top, bottom = n, n + 1

        parent = list(range(n + 2))
        rank = [0] * (n + 2)
        land = [False] * n

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(a: int, b: int) -> None:
            a, b = find(a), find(b)
            if a == b:
                return
            if rank[a] < rank[b]:
                parent[a] = b
            elif rank[a] > rank[b]:
                parent[b] = a
            else:
                parent[b] = a
                rank[a] += 1

        for d in range(len(cells) - 1, -1, -1):
            r, c = cells[d][0] - 1, cells[d][1] - 1
            idx = r * col + c
            land[idx] = True

            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < row and 0 <= nc < col:
                    nid = nr * col + nc
                    if land[nid]:
                        union(idx, nid)

            if r == 0:
                union(idx, top)
            if r == row - 1:
                union(idx, bottom)

            if find(top) == find(bottom):
                return d

        return 0


#################


###############
'''
another short but strange solution
'''


class Solution:
    def latestDayToCross(self, r: int, c: int, a: List[List[int]]) -> int:
        def check(k):
            def dfs(i, j, g={*map(tuple, a[:k + 1])}):
                if not (0 < i <= r and 0 < j <= c) or (i, j) in g: return 1  # stuck
                if i == r: return 0  # pass
                g.add((i, j))
                return all(starmap(dfs, ((i, j + 1), (i + 1, j), (i - 1, j), (i, j - 1))))

            return all(dfs(1, j + 1) for j in range(c))

        return bisect_left(range(len(a)), 1, key=check)
##################


if __name__ == '__main__':
    row = 13
    col = 9

    cells = [[12, 6], [3, 4], [2, 9], [9, 4], [9, 2], [6, 4], [4, 4], [8, 6], [4, 9], [5, 6], [7, 5], [12, 4], [11, 8],
             [3, 7], [2, 6], [9, 8], [3, 5], [13, 4], [1, 3], [10, 2], [8, 9], [6, 6], [11, 7], [11, 1], [13, 9],
             [12, 7], [10, 7], [8, 2], [1, 8], [7, 3], [6, 5], [2, 1], [10, 6], [4, 8], [4, 2], [9, 7], [6, 2], [3, 6],
             [12, 2], [10, 3], [10, 5], [9, 5], [8, 8], [8, 7], [3, 2], [13, 6], [3, 1], [5, 1], [2, 7], [8, 3],
             [12, 5], [11, 2], [6, 3], [1, 4], [13, 3], [4, 1], [9, 9], [7, 7], [4, 3], [12, 1], [2, 2], [7, 6], [4, 6],
             [7, 9], [7, 2], [3, 8], [1, 6], [11, 3], [11, 4], [5, 9], [13, 8], [1, 9], [10, 1], [9, 1], [6, 1],
             [10, 9], [12, 9], [11, 5], [8, 1], [13, 5], [9, 6], [13, 2], [6, 8], [2, 8], [5, 3], [3, 3], [13, 1],
             [11, 9], [9, 3], [2, 4], [5, 2], [8, 5], [13, 7], [12, 8], [5, 5], [7, 1], [7, 4], [2, 5], [6, 9], [4, 7],
             [5, 8], [1, 5], [10, 8], [8, 4], [1, 1], [3, 9], [1, 2], [7, 8], [1, 7], [6, 7], [11, 6], [4, 5], [5, 7],
             [2, 3], [10, 4], [5, 4], [12, 3]]

    row = 127
    col = 7

    cells = [[52, 3], [92, 3], [51, 4], [98, 3], [7, 2], [114, 7], [54, 3], [30, 1], [17, 3], [67, 2], [59, 5], [7, 4],
             [60, 5], [51, 3], [44, 3], [111, 5], [75, 1], [4, 1], [83, 2], [122, 4], [113, 5], [105, 2], [93, 6],
             [63, 2], [101, 5], [31, 6], [60, 6], [77, 7], [108, 3], [22, 6], [10, 3], [42, 6], [18, 1], [62, 7],
             [47, 7], [43, 6], [2, 1], [41, 3], [107, 2], [52, 2], [119, 4], [23, 7], [95, 6], [29, 3], [38, 7],
             [17, 5], [123, 3], [7, 1], [62, 4], [40, 6], [49, 2], [31, 4], [17, 1], [89, 2], [102, 2], [58, 4],
             [109, 6], [18, 5], [3, 1], [107, 3], [15, 6], [20, 2], [90, 4], [35, 6], [33, 6], [100, 6], [4, 7],
             [123, 5], [75, 6], [43, 1], [19, 1], [123, 7], [103, 3], [126, 4], [84, 6], [69, 7], [58, 6], [71, 5],
             [51, 6], [23, 5], [85, 3], [87, 6], [116, 2], [76, 3], [36, 5], [32, 3], [19, 3], [5, 4], [28, 4], [71, 7],
             [117, 5], [19, 4], [32, 1], [118, 4], [53, 3], [78, 1], [76, 7], [122, 5], [57, 7], [32, 7], [124, 4],
             [119, 7], [106, 5], [44, 1], [16, 4], [34, 3], [106, 4], [6, 2], [70, 5], [62, 5], [23, 3], [76, 5],
             [91, 3], [31, 3], [43, 4], [36, 1], [39, 1], [18, 3], [100, 4], [48, 2], [1, 6], [83, 7], [88, 1], [66, 5],
             [119, 3], [4, 6], [104, 7], [101, 4], [31, 7], [38, 4], [65, 5], [124, 1], [22, 3], [51, 2], [100, 7],
             [1, 4], [16, 3], [80, 2], [127, 4], [25, 1], [108, 7], [96, 3], [51, 5], [56, 5], [67, 3], [29, 4],
             [43, 2], [31, 5], [11, 5], [115, 1], [96, 6], [60, 7], [80, 3], [33, 4], [13, 5], [102, 4], [114, 2],
             [111, 3], [112, 1], [39, 2], [56, 2], [8, 4], [23, 6], [126, 3], [71, 6], [110, 7], [2, 4], [101, 3],
             [80, 6], [108, 6], [55, 5], [75, 4], [63, 4], [46, 7], [112, 3], [72, 3], [37, 4], [37, 7], [12, 1],
             [106, 2], [93, 7], [65, 7], [127, 6], [57, 4], [4, 3], [58, 1], [102, 7], [91, 7], [62, 3], [65, 6],
             [70, 1], [59, 7], [92, 2], [75, 5], [84, 2], [35, 2], [63, 1], [86, 2], [122, 6], [111, 1], [27, 6],
             [35, 4], [84, 7], [67, 5], [80, 5], [87, 3], [41, 4], [34, 1], [72, 2], [46, 3], [99, 1], [16, 1], [66, 7],
             [17, 2], [79, 3], [102, 5], [81, 4], [93, 4], [108, 2], [7, 5], [77, 5], [97, 2], [120, 2], [55, 3],
             [127, 3], [109, 3], [88, 7], [87, 4], [37, 5], [118, 2], [111, 4], [14, 3], [40, 5], [69, 2], [23, 1],
             [79, 1], [115, 7], [73, 6], [98, 1], [88, 6], [65, 1], [61, 5], [66, 4], [41, 5], [20, 3], [104, 1],
             [110, 4], [11, 6], [44, 4], [24, 4], [47, 1], [91, 5], [61, 3], [16, 7], [21, 5], [59, 6], [127, 5],
             [94, 6], [17, 4], [2, 2], [46, 4], [54, 1], [32, 4], [36, 3], [67, 6], [125, 4], [27, 4], [93, 1],
             [103, 4], [8, 6], [89, 1], [27, 5], [83, 3], [22, 1], [48, 5], [114, 5], [126, 6], [52, 4], [113, 7],
             [44, 5], [82, 5], [114, 3], [72, 1], [8, 3], [11, 7], [22, 5], [49, 4], [27, 1], [121, 3], [53, 6],
             [77, 2], [18, 4], [95, 1], [84, 4], [12, 7], [114, 4], [126, 5], [6, 1], [43, 3], [74, 6], [30, 5],
             [58, 5], [11, 2], [70, 2], [30, 6], [19, 6], [42, 3], [7, 3], [15, 5], [125, 7], [98, 6], [40, 4], [39, 6],
             [42, 2], [17, 7], [87, 2], [45, 5], [103, 7], [96, 4], [109, 5], [89, 6], [86, 5], [107, 7], [76, 6],
             [47, 2], [52, 5], [39, 7], [50, 1], [48, 1], [16, 2], [4, 4], [81, 1], [97, 1], [63, 7], [71, 3], [68, 4],
             [76, 1], [121, 6], [15, 2], [69, 4], [81, 3], [86, 3], [45, 7], [92, 6], [33, 2], [82, 2], [71, 1],
             [50, 2], [57, 6], [87, 7], [30, 4], [105, 1], [55, 4], [90, 2], [106, 7], [125, 5], [124, 7], [27, 2],
             [88, 3], [106, 1], [69, 3], [58, 2], [107, 4], [64, 2], [107, 6], [56, 3], [67, 4], [95, 4], [1, 5],
             [45, 6], [50, 3], [50, 4], [56, 4], [74, 4], [37, 3], [73, 7], [125, 3], [86, 1], [92, 4], [31, 2], [9, 3],
             [14, 6], [68, 6], [66, 2], [38, 3], [81, 7], [55, 6], [116, 3], [21, 4], [23, 4], [6, 4], [1, 1], [14, 4],
             [116, 7], [26, 2], [118, 1], [101, 6], [28, 2], [110, 6], [36, 2], [127, 1], [99, 4], [78, 5], [21, 6],
             [118, 3], [54, 5], [54, 7], [59, 4], [26, 1], [3, 5], [69, 6], [3, 4], [77, 1], [64, 5], [104, 6],
             [119, 5], [28, 6], [1, 2], [122, 7], [52, 7], [114, 1], [127, 7], [103, 1], [115, 6], [78, 7], [6, 7],
             [56, 6], [109, 2], [25, 5], [91, 6], [108, 1], [54, 4], [7, 6], [11, 3], [12, 5], [115, 2], [38, 1],
             [113, 2], [92, 1], [42, 7], [87, 5], [70, 7], [36, 6], [102, 1], [98, 7], [81, 6], [72, 7], [111, 7],
             [42, 1], [64, 1], [126, 7], [99, 7], [122, 3], [80, 1], [112, 2], [8, 7], [113, 6], [104, 4], [118, 7],
             [72, 6], [98, 5], [10, 2], [78, 6], [46, 5], [113, 3], [84, 1], [113, 1], [85, 7], [68, 2], [80, 4],
             [30, 3], [8, 5], [41, 1], [30, 7], [124, 5], [15, 1], [43, 5], [69, 5], [105, 7], [96, 2], [40, 3],
             [25, 7], [63, 6], [38, 2], [61, 1], [107, 5], [2, 3], [85, 6], [123, 6], [14, 7], [53, 5], [121, 5],
             [112, 6], [117, 7], [31, 1], [42, 5], [20, 1], [2, 7], [12, 4], [5, 3], [53, 2], [14, 2], [89, 4], [52, 6],
             [117, 3], [125, 6], [97, 5], [32, 2], [22, 7], [40, 7], [126, 1], [63, 3], [72, 4], [34, 7], [6, 6],
             [77, 6], [93, 5], [12, 2], [115, 4], [120, 4], [124, 2], [20, 6], [116, 4], [49, 7], [79, 2], [121, 1],
             [47, 5], [64, 7], [4, 2], [73, 4], [94, 1], [60, 2], [26, 6], [75, 7], [122, 1], [90, 1], [119, 6],
             [41, 2], [18, 2], [13, 7], [87, 1], [53, 4], [74, 2], [93, 3], [82, 7], [55, 7], [124, 6], [58, 7],
             [21, 7], [35, 5], [29, 7], [103, 6], [45, 1], [27, 3], [20, 7], [105, 4], [33, 5], [26, 5], [79, 5],
             [116, 6], [91, 2], [23, 2], [15, 3], [104, 3], [19, 7], [44, 2], [86, 6], [97, 6], [112, 4], [121, 2],
             [29, 6], [80, 7], [48, 4], [110, 2], [10, 6], [78, 2], [28, 3], [94, 7], [13, 6], [88, 2], [61, 2],
             [66, 1], [39, 4], [68, 5], [69, 1], [39, 5], [15, 4], [79, 4], [59, 1], [78, 4], [98, 4], [83, 4], [99, 6],
             [120, 3], [110, 5], [90, 7], [90, 3], [126, 2], [76, 4], [53, 7], [26, 7], [67, 1], [66, 6], [117, 2],
             [88, 4], [124, 3], [70, 3], [82, 3], [24, 7], [19, 2], [60, 1], [10, 4], [125, 2], [64, 6], [51, 7],
             [86, 7], [114, 6], [50, 5], [22, 2], [1, 7], [102, 6], [59, 2], [46, 1], [96, 1], [88, 5], [6, 3],
             [109, 7], [123, 4], [121, 4], [45, 3], [109, 4], [97, 3], [50, 7], [112, 5], [68, 1], [68, 7], [113, 4],
             [14, 5], [49, 5], [7, 7], [89, 3], [34, 2], [20, 5], [35, 3], [94, 5], [50, 6], [29, 5], [65, 4], [108, 4],
             [85, 2], [73, 3], [34, 6], [94, 3], [21, 1], [97, 7], [42, 4], [3, 7], [25, 3], [70, 4], [5, 2], [2, 6],
             [61, 7], [20, 4], [26, 3], [100, 3], [103, 5], [48, 3], [89, 7], [54, 6], [24, 6], [111, 6], [61, 4],
             [21, 2], [32, 5], [64, 3], [85, 5], [116, 1], [11, 4], [111, 2], [25, 4], [45, 4], [11, 1], [81, 5],
             [118, 5], [3, 2], [70, 6], [54, 2], [9, 6], [120, 1], [110, 3], [28, 7], [34, 4], [62, 2], [105, 5],
             [83, 6], [25, 6], [5, 7], [10, 7], [95, 5], [63, 5], [35, 7], [28, 1], [90, 6], [95, 7], [33, 1], [57, 2],
             [55, 1], [64, 4], [37, 6], [76, 2], [73, 2], [1, 3], [24, 5], [51, 1], [43, 7], [92, 7], [71, 2], [83, 1],
             [98, 2], [9, 1], [9, 7], [79, 6], [60, 4], [108, 5], [116, 5], [21, 3], [117, 1], [102, 3], [103, 2],
             [47, 3], [29, 2], [101, 2], [122, 2], [34, 5], [47, 4], [44, 6], [12, 6], [91, 4], [77, 4], [105, 3],
             [105, 6], [19, 5], [100, 1], [74, 3], [119, 2], [97, 4], [82, 6], [49, 1], [84, 5], [8, 1], [65, 2],
             [120, 6], [127, 2], [123, 2], [95, 3], [13, 2], [101, 7], [73, 1], [73, 5], [17, 6], [13, 3], [95, 2],
             [104, 5], [5, 5], [33, 3], [106, 6], [52, 1], [89, 5], [40, 1], [123, 1], [83, 5], [85, 4], [13, 1],
             [13, 4], [86, 4], [4, 5], [104, 2], [120, 7], [16, 5], [39, 3], [99, 2], [9, 2], [68, 3], [91, 1], [25, 2],
             [2, 5], [119, 1], [77, 3], [109, 1], [28, 5], [55, 2], [46, 6], [75, 3], [74, 7], [94, 2], [59, 3],
             [93, 2], [106, 3], [48, 6], [40, 2], [45, 2], [112, 7], [72, 5], [81, 2], [99, 3], [5, 6], [33, 7],
             [41, 6], [79, 7], [56, 7], [60, 3], [5, 1], [74, 1], [29, 1], [101, 1], [6, 5], [115, 5], [49, 3],
             [125, 1], [32, 6], [66, 3], [53, 1], [74, 5], [62, 6], [3, 3], [57, 1], [118, 6], [100, 5], [12, 3],
             [3, 6], [9, 4], [41, 7], [82, 1], [96, 7], [18, 6], [49, 6], [24, 2], [57, 3], [9, 5], [78, 3], [71, 4],
             [18, 7], [94, 4], [110, 1], [90, 5], [65, 3], [121, 7], [35, 1], [67, 7], [117, 6], [75, 2], [85, 1],
             [24, 1], [48, 7], [44, 7], [58, 3], [26, 4], [36, 4], [38, 6], [15, 7], [10, 1], [47, 6], [99, 5], [24, 3],
             [56, 1], [115, 3], [37, 2], [62, 1], [120, 5], [96, 5], [100, 2], [38, 5], [30, 2], [107, 1], [27, 7],
             [82, 4], [37, 1], [16, 6], [36, 7], [10, 5], [84, 3], [22, 4], [61, 6], [92, 5], [117, 4], [14, 1],
             [57, 5], [8, 2], [46, 2]]

    road = makeRoad(row, col, cells)
    checkRoad(road, cells)

    day = 35
    day = 195

    print(f"now check selected path, transpose for better visual")

    checkRoadD(transpose(road), day)

    print(f"result of limit at day: {day} is: {dayDFSDriver(road, day)}")
    # print(f"final res: {binarySearch(road, row*col)}")
