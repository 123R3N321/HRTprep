'''
goal:
solve lc460 lfu

workup:
lc146 lru (easy for me)
lc895 max freq stack (huh?)
'''

from collections import OrderedDict

'''
LRU simple Ordereddict
'''


class LRUCache:

    def __init__(self, capacity: int):
        self.n = capacity
        self.d = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.d: return -1
        self.d.move_to_end(key)  # indicate most recent use
        return self.d[key]

    def put(self, key: int, value: int) -> None:
        if key in self.d:  # easy
            self.d.move_to_end(key)
            self.d[key] = value  # value update
        else:
            if self.n > 0:
                self.n -= 1
            else:
                self._evict()
            self.d[key] = value  # add the entry

    def _evict(self):
        self.d.popitem(False)  # pop from front


'''
ok that was really, really easy
now move on to lc895
'''
'''
double dict of:
    val -- freq
    freq -- set of vals
        when freq goes up, add to entry (auto most recent)
        when freq goes down, remove from old freq entry then do nothing
    the beauty is that when removing, we first check if there
    are other entries in the freq-set dict,
    if not we simply need to query the one lower freq (guaranteed to exist)
'''


class FreqStack:

    def __init__(self):
        self.d = dict()  # key: val, value: freq
        self.fd = dict()  # key: freq, value: list of values of that freq
        self.top = 0  # when starting, top freq is 0

    def push(self, val: int) -> None:
        if val not in self.d:
            self.d[val] = 1
        else:
            self.d[val] += 1
        freq = self.d[val]
        if freq not in self.fd:
            self.fd[freq] = []
        self.fd[freq].append(val)
        self.top = max(self.top, freq)

    def pop(self) -> int:
        # assume always legal
        res = self.fd[self.top].pop()
        self.d[res] -= 1
        if not self.fd[self.top]:
            self.top -= 1
        return res


'''
okie, this wasn't that hard either. If I see it again it
will be very easy.

Ultimate challenge: LFU


after checking solutions:
okie, not hard. But indeed very long code
'''


class Node:
    def __init__(self, key, val):  # val is frequency
        self.prev = None
        self.next = None
        self.key = key
        self.val = val
        self.freq = 1


class Dll:
    def __init__(self) -> None:
        self.header = None
        self.trailer = None
        self.n = 0

    def add(self, node):  # add front
        node.prev = None
        node.next = None  # cleanse
        self.n += 1
        if self.n == 1:
            self.header = self.trailer = node
            return
        else:
            node.next = self.header
            self.header.prev = node
            self.header = node

    def pop(self, node=None):  # return popped node, pop back
        if self.n <= 0: return  # do nothing
        self.n -= 1
        if node is None:
            node = self.trailer
        prevNode = node.prev
        nextNode = node.next
        if prevNode is None:
            self.header = nextNode
        else:
            prevNode.next = nextNode

        if nextNode is None:
            self.trailer = prevNode
        else:
            nextNode.prev = prevNode

        node.prev = None
        node.next = None
        return node


from collections import defaultdict


class LFUCache:

    def __init__(self, capacity: int):
        self.lf = 0
        self.cap = capacity
        self.n = capacity
        self.nd = dict()  # key: key, val: node
        self.fd = defaultdict(Dll)  # key: freq, val: dll of nodes

    def get(self, key: int) -> int:
        if key not in self.nd: return -1
        res = self.nd[key].val
        node = self.nd[key]
        self._update(node)
        return res

    def put(self, key: int, value: int) -> None:
        if self.cap <= 0: return
        if key in self.nd:
            node = self.nd[key]
            node.val = value
            self._update(node)
            return
        else:  # add new node, update n, lf, nd, fd
            if self.n == 0:
                self._evict()
            else:
                self.n -= 1  # indicate quota used
            node = Node(key, value)  # create new node
            self.fd[1].add(node)  # add to freq 1 dll
            self.nd[key] = node
            self.lf = 1

    def _update(self, node):
        oldFreq = node.freq
        self.fd[oldFreq].pop(node)  # remove from old dll

        freq = oldFreq + 1
        node.freq = freq
        self.fd[freq].add(node)  # add to new dll

        if self.lf == oldFreq and self.fd[oldFreq].n <= 0:
            # del self.fd[oldFreq]
            self.lf = freq

    def _evict(self):
        victim = self.fd[self.lf].pop()  # kill victim
        if victim is None: return
        del self.nd[victim.key]
        # note we have not updated self.lf yet


