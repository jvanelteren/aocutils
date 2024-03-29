# AUTOGENERATED! DO NOT EDIT! File to edit: ../04_special.ipynb.

# %% auto 0
__all__ = ['md5', 'binarysearch', 'deduce_matches', 'find_specific_pattern', 'find_repeat', 'find_cycle', 'UnionFind', 'Octree',
           'LazySegmentTree', 'Trie']

# %% ../04_special.ipynb 2
import hashlib
from pathlib import Path
import networkx as nx
from collections import defaultdict
from dataclasses import dataclass
from aocutils.common import ints
from collections import namedtuple
import heapq

# %% ../04_special.ipynb 3
def md5(input):
    return hashlib.md5(input.encode('utf-8')).hexdigest()

# %% ../04_special.ipynb 5
def binarysearch(minim,maxim,function, flips_to_true=True, verbose=True): 
    """
     function needs to return a boolean whether the solution is ok
     this implementation is for function that starts with false for minim and flip to true
     for TTTTFFFF, pass set flips_to_true flag to false. This flag is important to set correct!
    """
    new = minim
    while True:
        new = (minim+maxim)//2
        if verbose: print(f'to_test: {new}, min {minim}, max {maxim} ', end=' ')
        res = function(new)
        if verbose: print('function returns', res)
        if not flips_to_true: res = not res
        if res:
            if new == maxim: # solution found
                if flips_to_true:
                    print('solution found',new)
                    return new
                else:
                    print('solution found',new-1)
                    return new-1
            maxim = new
        else: minim = new+1


# %% ../04_special.ipynb 7
def deduce_matches(input_dict):
    """
    Takes a dict with multiple keys that have one or more options
    The trick is to start with what you know: keys with one option and remove that option for the other keys
    Continuing that process leads to every key ending up with one option (hopefully)
    """
    
    for v in input_dict.values():
        # Checks the first element of iterable to infer the option type (e.g. string or tuple)
        option_type = type(v[0])
        break
    
    found = 0
    while found < len(input_dict):
        for k, v in input_dict.items():
            if not isinstance(v, option_type) and len(v) == 1: # found one
                to_rem = v.pop()
                input_dict[k] = to_rem
                found += 1
                for _ , v2 in input_dict.items(): # remove the item from other lists
                    if not isinstance(v2, option_type) and to_rem in v2:
                        v2.remove(to_rem)
    return input_dict

# %% ../04_special.ipynb 9
def find_specific_pattern(start_pattern, function, goal = None, n_iter=1000000000):
    """
        Returns when a SPECIFIED pattern has been found from a function
        If goal = None, then first time the start pattern shows up again is returned
        Returns steps, pattern
    """
    if not goal: goal = start_pattern
    current = start_pattern
    for i in range(1,n_iter):
        current = function(current)
        # print(current)
        if current == goal:
            print(f'At step {i}, goal: {current} was found')
            return i

# %% ../04_special.ipynb 10
def find_repeat(start_pattern, function, n_iter=None):
    """
        Returns when a NONSPECFIED repeating pattern has been found
        Returns steps, pattern
    """
    if not n_iter: n_iter = round(10e20)
    seen = {start_pattern}
    current = start_pattern
    for i in range(1,n_iter):
        current = function(current)
        # print(current)
        if current in seen:
            print(f'Repeat was found at step {i}. Pattern: {current} returning steps, pattern')
            return i,current
        seen.add(current)

# %% ../04_special.ipynb 11
def find_cycle(start_pattern, function):
    """
        Find cycle length of some repeating pattern, by first inspecting which item repeats when
        And subtracting the time the item was first seen
    """
    step_second, pattern = find_repeat(start_pattern, function)
    step_first = find_specific_pattern(start_pattern, function, goal = pattern)
    return step_second - step_first

# %% ../04_special.ipynb 15
class UnionFind():
    # should have unique objects
    def __init__(self, it):
        self.parents = {obj:obj for obj in it}
        self.sizes = {obj:1 for obj in it}
        assert len(it) == len(self.parents), 'does your iterable contain duplicates?'
        
    def add(self, obj):
        # add a new object after instantiation, returns False if object already in
        if obj not in self.parents:
            self.parents[obj] = obj
            self.sizes[obj] = 1
            return True
        return False
        
    def get_parent(self, x):
        # finding the parent of an object
        while x != self.parents[x]:
            parent = self.parents[x]
            # path compression
            self.parents[x] = self.parents[parent]
            x = parent
        return x
        
    def union(self,x,y):
        # unions two objects, returns False if items have the same parent and are therefore already in the same group
        for i in (x,y):
            if i not in self.parents:
                self.add(i)
                
        x,y  = self.get_parent(x), self.get_parent(y)
        if x == y:
            return False
        if self.sizes[x] < self.sizes[y]:
            # make sure that x is the largest group
            x, y = y, x
        self.parents[y] = x
        self.sizes[x] += self.sizes[y]
        self.sizes[y] = 0
    
    def groups(self):
        # returns all linked objects in a list of lists
        groups = defaultdict(list)
        for i in self.parents:
            groups[self.get_parent(i)].append(i)
        return list(groups.values())

    def is_spanning(self):
        return len(self.groups()) == 1

# %% ../04_special.ipynb 17
@dataclass
class Octree():
    # 2018 day 23. Takes a huge space and that can be recursively partitioned
    left:int
    right:int
    up:int
    leftrange:int
    rightrange:int
    uprange:int
    totalhits:int=0
    
    def split(self):
        midl = self.left + self.leftrange //2 + 1
        midr = self.right + self.rightrange //2 + 1
        midu = self.up + self.uprange // 2 + 1
        for l in (self.left, midl):
            for r in (self.right, midr):
                for u in (self.up, midu):
                    yield Octree(l,r,u,self.leftrange//2, self.rightrange//2, self.uprange//2)
   
    def hits(self, other):
        # checks if Octree square is in range of a Robot (distance < power of robot)
        dis = 0
        dis += max(0, self.left - other.l, other.l - (self.left + self.leftrange))
        dis += max(0, self.right - other.r, other.r - (self.right + self.rightrange))
        dis += max(0, self.up - other.u, other.u - (self.up + self.uprange))
        return dis <= other.p
    
    def count(self, others):
        # expects an iterable of Robots
        self.distance = (abs(self.left) + abs(self.right) + abs(self.up))
        self.totalhits = -sum(self.hits(o) for o in others)
    
    def __gt__(self,other):
        # compares itself to other Octrees. Better is more hits, smaller size and shorter distance from origin
        return (self.totalhits, self.leftrange, self.distance) > (other.totalhits, other.leftrange, other.distance)
    


# %% ../04_special.ipynb 19
class LazySegmentTree():
    # based on https://leetcode.com/problems/my-calendar-iii/solution/
    # lazy: the number of events covering all times in the range. As all numbers that belong to this range will be added by some increment, we don't have to propagate the base increment to every time in the interval, all we need to do is putting the number in this lazy field. 
    # We only update val by adding lazy when requested to query the max numbers of intervals in [L, R].
    def __init__(self, left, right) -> None:
        self.left, self.right = left, right # detailing the range of interest
        self.idxs = defaultdict(int)
        self.lazy = defaultdict(int)
        
    def add(self, start, end, l=None,r=None, idx=1):
        if l == None:
            l = self.left
        if r == None:
            r = self.right
        if l > end or r < start:
            return
        elif l >= start and r <= end and l <=r:
            self.idxs[idx] += 1
            self.lazy[idx] += 1
        else:
            mid = (l + r) // 2
            self.add(start, end, l, mid, idx*2)
            self.add(start, end, mid+1, r, idx*2 + 1)
            self.idxs[idx] = self.lazy.get(idx,0) + max((self.idxs.get(idx*2,0),self.idxs.get(idx*2+1,0)))
            
    def getbest(self):
        return self.idxs[1]

# %% ../04_special.ipynb 21
def Trie():
    return defaultdict(Trie)
