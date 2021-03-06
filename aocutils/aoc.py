# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['load', 'save', 'DATA_DIR', 'to_int', 'flatten', 'md5', 'arr_to_dict', 'reverse_dict', 'untar_data',
           'timeit', 'nan_inspect', 'neighbors', 'arr_neighbors', 'dimensions', 'Dim', 'positive', 'manhattan',
           'conv1d', 'conv2d', 'binarysearch', 'deduce_matches', 'bfs', 'dijkstra', 'get_path', 'dfs',
           'find_pattern_in_iter', 'find_repeat', 'find_cycle', 'factors']

# Cell
from collections.abc import Iterable
from collections import namedtuple, deque
import contextlib
import copy
from functools import reduce
import hashlib
import heapq
import logging
from math import sqrt, gcd
from pathlib import Path
import time

import pandas as pd
import numpy as np

# Cell
import pickle

DATA_DIR = Path('data')
def load(filename):
    f = open(DATA_DIR/filename,"rb")
    return pickle.load(f)

def save(data, filename):
    with open(DATA_DIR/filename, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Cell
def to_int(inp):
    """
        returns items converted to int if possible also works for tuples\n
        also works recursively
        watch out because passing a string '12t' will be ripped into a list [1,2,t]
    """
    if isinstance(inp,str):
        print('watch out string will be converted into list of characters')
    if isinstance(inp[0],list):
        return list(to_int(l) for l in inp)
    if isinstance(inp[0],tuple):
        return tuple(to_int(l) for l in inp)

    out = []
    for i in inp:
        try:
            out.append(int(i))
        except ValueError:
            out.append(i)
    if isinstance(inp,tuple): return tuple(out)
    else: return list(out)

# Cell

def flatten(x):
    # recursive flattens the input. Returns a list
    return list(_flatten(x))

def _flatten(x):
    for item in x:
        if isinstance(item,Iterable) and not isinstance(item, str):
            yield from flatten(item)
        else:
            yield item

# Cell
def md5(input):
    return hashlib.md5(input.encode('utf-8')).hexdigest()


# Cell
def arr_to_dict(arr):
    """
        takes in an numpy array or list and returns a dictionary with indices, values
    """
    d = {}
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            d[(i,j)] = arr[i][j]
    return d


# Cell
def reverse_dict(d):
    return {v:k for k,v in d.items()}

# Cell
def untar_data(path, save_dir = None):
    # will untar a file to save dir or the directory of path
    if isinstance(path,Path):
        if str(path).endswith("tgz"):
            tar = tarfile.open(fname, "r:gz")
        else:
            tar = open(path)
        tar.extractall(save_dir) if save_dir else tar.extractall(path.parent)
        tar.close()
    else:
        print('argument should be Path instance')

# Cell
logging.getLogger().setLevel(logging.INFO)
@contextlib.contextmanager
def timeit(description=None):
    # usage: with timeit('description') do what you like
    # will output the time taken in seconds
    tstart = time.time()
    yield
    elapsed = (time.time() - tstart)/60
    logging.info(f'{description}, time: {elapsed}')


# Cell
def nan_inspect(df):
    # will return some sort or correlation matrix
    # this helps to quickly see where the na values are and if they are shared with multiple columns
    print(df.isnull().sum(axis=1).value_counts(sort=False))
    df_len = len(df)
    df = df.isna().copy()
    df = df.loc[:, (df != 0).any(axis=0)]
    df = df.loc[(df!=0).any(1)]
    df_nan_dict = {c : [len(df.loc[df[c] & df[c2]]) for c2 in df.columns] for c in df.columns}
    df_nan = pd.DataFrame.from_dict(df_nan_dict)
    df_nan.set_index(df.columns, inplace=True)
    df_nan.insert(0, 'total', df_nan.max(axis=0))
    df_nan.sort_values('total', inplace=True, ascending=False)
    df_nan = pd.concat([df_nan['total'] , df_nan.iloc[:,1:][list(df_nan.index)]],axis=1)
    return (df_nan/df_len).round(2)

# Cell
def neighbors(i, diag = True,inc_self=False):
    """
     determine the neighbors, returns a set with neighboring tuples {(0,1)}
     if inc_self: returns self in results
     if diag: return diagonal moves as well
    """
    r = [1,0,-1]
    c = [1,-1,0]
    if diag:
        if inc_self:
            return {(i[0]+dr, i[1]+dc) for dr in r for dc in c}
        else:
            return {(i[0]+dr, i[1]+dc) for dr in r for dc in c if not (dr == 0 and dc == 0)}
    else:
        res =  {(i[0],i[1]+1), (i[0],i[1]-1),(i[0]+1,i[1]),(i[0]-1,i[1])}
        if inc_self: res.add(i)
        return res

# Cell
def arr_neighbors(arr, diag=True, inc_self=False):
    """
    Returns a dictionary with index: set of neighbor indices
    Parameters: diag to include diagonal neighbors, inc_self to include self in result list
    Usage: for index, neighbor_indices in aoc.arr_neighbors(arr).items():
    """
    res = {}
    for i in np.ndindex(arr.shape):
        # print('hi',i, neighbors(i,diag))
        res[i] = {(x,y) for x,y in neighbors(i,diag, inc_self) if 0<=x<arr.shape[0] and 0<=y<arr.shape[1]}
    return res


# Cell

Dim = namedtuple('Dim',['min','max','range'])
def dimensions(obj):
    """
     takes an iterable of iterables and returns a namedtuple with minima, maxima and range
     for example a 2d numpy array
     dim.min, dim.max and dim.range
    """
    minim = tuple(min(obj,key = lambda x:x[i])[i] for i in range(len(obj[0])))
    maxim = tuple(max(obj,key = lambda x:x[i])[i] for i in range(len(obj[0])))# max for dimensions
    ranges = tuple(maxim[i] - minim[i]  for i in range(len(obj[0])))
    res = Dim(minim,maxim,ranges)
    return res

# Cell
def positive(*args):
    """
        takes 1 or multiple lists of n coordinates and returns it normalized (getting rid of negatives)
    """
    dtype = type(args[0][0]) # support list(s) of lists and list(s) of tuples
    if len(args)==1: # only 1 argument passed
        dim = dimensions(args[0])
        obj = args[0]
        if dtype == tuple:
            return [tuple(o[i]-dim.min[i] for i in range(len(obj[0]))) for o in obj]
        if dtype == list:
            return [[o[i]-dim.min[i] for i in range(len(obj[0]))] for o in obj]
        else: print('no support for dtype',dtype)
    else: # multiple arguments passed
        dim = dimensions([i for a in args for i in a])
        if dtype == tuple:
            return ([tuple(o[i]-dim.min[i] for i in range(len(obj[0]))) for o in obj] for obj in args)

        if dtype == list:
            return ([[o[i]-dim.min[i] for i in range(len(obj[0]))] for o in obj] for obj in args)
        else: print('no support for dtype',dtype)


# Cell
def manhattan(x,y):
    return abs(x[0]-y[0])+abs(x[1]-y[1])

# Cell
def conv1d(arr,conv_shape,mode='same',padding=None,pad_dir='center') ->list:
    """
    Returns a list of kernel views of a string or list
    mode == 'valid': returns only results where the kernel fits
    mode == 'same': return the same amount of items as original
    when mode =='same', default padding is the outer value
    """
    if padding:
        to_pad = padding # user specified padding
    else:
        to_pad = arr[0] # begin or end of list

    if isinstance(arr,list): # to convert a list temporarily to string
        arr_is_list = True
    else:
        arr_is_list = False

    if mode == 'valid':
        pass

    p_size = conv_shape//2
    if mode == 'same':
        if arr_is_list:
            arr = ''.join(arr)
        if isinstance(arr,str): #here the padding is applied
            if pad_dir == 'center':
                arr = to_pad*p_size+arr+to_pad*p_size
            if pad_dir == 'left':
                arr = to_pad*(conv_shape-1)+arr
            if pad_dir == 'right':
                arr = arr+to_pad*(conv_shape-1)
        else:
            return 'only string and list supported'
        if arr_is_list:
            arr = list(arr)

    if conv_shape % 2 == 1: # odd conv_shape
        return [arr[i-p_size:i+p_size+1] for i in range(p_size,len(arr)-p_size)]
    else: # even conv_shape
        return [arr[i:i+conv_shape] for i in range(0,len(arr)-conv_shape+1)]


# Cell
def conv2d(arr,conv_shape,mode='valid',padding=None,pad_dir='center') ->list:
    """
    Returns a list of kernel views of a string or list
    mode == 'valid': returns only results where the kernel fits
    mode == 'same': return the same amount of items as original
    when mode =='same', default padding is the outer value
    """
    if padding:
        to_pad = padding # user specified padding
    else:
        to_pad = arr[0] # begin or end of list

    if isinstance(arr,list) or isinstance(arr,np.ndarray): # to convert a list to numpy array
        arr_is_list = True
    else:
        arr_is_list = False

    if mode == 'valid':
        pass

    p_size = conv_shape//2
    if mode == 'same':
        if arr_is_list:
            arr = np.array(arr)
        if isinstance(arr,str): #here the padding is applied
            if pad_dir == 'center':
                arr = to_pad*p_size+arr+to_pad*p_size
            if pad_dir == 'left':
                arr = to_pad*(conv_shape-1)+arr
            if pad_dir == 'right':
                arr = arr+to_pad*(conv_shape-1)
        else:
            return 'only string and list supported'
        if arr_is_list:
            arr = list(arr)

    if conv_shape % 2 == 1: # odd conv_shape
        return [arr[i-p_size:i+p_size+1] for i in range(p_size,len(arr)-p_size)]
    else: # even conv_shape
        return [arr[i:i+conv_shape] for i in range(0,len(arr)-conv_shape+1)]


# Cell

def binarysearch(minim,maxim,function, flips_to_true=True):
    """
     function needs to return a boolean whether the solution is ok
     this implementation is for function that starts with false for minim and flip to true
     for TTTTFFFF, pass set flips_to_true flag to false. This flag is important to set correct!
    """
    new = minim
    while True:
        new = (minim+maxim)//2
        print(f'to_test: {new}, min {minim}, max {maxim} ', end=' ')
        res = function(new)
        print('function returns', res)
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


# Cell
def deduce_matches(input_dict, option_type=str):
    """
    Takes a dict with multiple keys that have one or more options
    The trick is to start with what you know: keys with one option and remove that option for the other keys
    Continuing that process leads to every key ending up with one option (hopefully)

    Assumes: the options are strings and sort in some kind of container
    """
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

# Cell
def bfs(connections, start, goal=None, verbose=False):
    """
    Requires a connections dict with tuples with neighbors per node.
    Or a connections function returning neighbors per node

    Returns
    if goal == None:    return dict of locations with neighbor closest to start
    elif goal found:    returns path to goal
    else:               returns False
    """
    seen = set() # the locations that have been explored
    frontier = deque([start]) # the locations that still need to be visited
    # paths = {start: [start]}
    isfunction = callable(connections)
    parents = {start: None}

    def get_path(parents,start,goal):
        # print(start,goals)
        cur = goal
        path = [cur]
        while cur != start:
            cur = parents[cur]
            path.append(cur)
        path.reverse()
        return path

    while frontier:
        search = frontier.popleft()
        if isfunction: neighbors = connections(search)
        else: neighbors = connections.get(search,None)
        if neighbors:
            for n in neighbors:
                if n not in seen:
                    seen.add(n)
                    frontier.append(n)
                    # paths[n] = paths[search]+[n]
                    parents[n]= search
                    if goal and n == goal:
                        # print('goal found')
                        return get_path(parents,start,goal)
                        # return paths[goal],parents
        seen.add(search)
    if goal: return False
    else: return parents

# Cell
def dijkstra(connections,start, goal=None):
    """
    Requires a dict with as values a LIST of tuples (neighbor, weight)
    Or a function returning a list of tuples with neighbors and weights per node

    Returns
    if goal == None:    return all paths from start
    elif goal found:    returns path to goal
    else:               returns False
    """
    seen = set() # the locations that have been explored
    frontier = [(0,start)] # the locations that still need to be visited
    isfunction = callable(connections)
    parents = {start: (None,0)}

    def get_path(parents):
        cur = goal
        path = [cur]
        cost = parents[cur][1]
        while cur != start:
            cur = parents[cur][0]
            path.append(cur)
        path.reverse()
        return path,cost

    while frontier:
        # print('\n\n',frontier,'\n',parents)
        search_cost, search_node = heapq.heappop(frontier)
        # print('looking for', search_node,search_cost)
        if search_node == goal: break
        if isfunction: neighbors = connections(search_node)
        else: neighbors = connections.get(search_node,None)
        if neighbors:
            for n in neighbors:
                # print('n',n)
                if n[0] not in parents or n[1]+ search_cost < parents[n[0]][1]:
                    # print('updating')
                    heapq.heappush(frontier,(search_cost+n[1],n[0]))
                    # paths[n] = paths[search_node]+[n]
                    parents[n[0]]= (search_node,search_cost+n[1])
                        # return paths[goal],parents
        seen.add(search_node)
    if not goal: return parents
    elif goal in parents: return get_path(parents)
    else: return False


# Cell
def get_path(parents,start,goal):
    # print(start,goals)
    cur = goal
    path = [cur]
    while cur != start:
        cur = parents[cur]
        path.append(cur)
    path.reverse()
    return path

# Cell
# found this on internet
def dfs(graph, start):
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    return visited

# Cell
def find_pattern_in_iter(start_pattern, function, goal = None, n_iter=1000000000):
    """
        Returns when a SPECIFIED pattern has been found from a function
        If goal = None, then first time the start pattern shows up again is returned
    """
    if not goal: goal = start_pattern
    current = start_pattern
    for i in range(1,n_iter):
        current = function(current)
        # print(current)
        if current == goal:
            print('found at step',i, current)
            return i, current

# Cell
def find_repeat(start_pattern, function, n_iter=None):
    """
        Returns when a NONSPECFIED repeating pattern has been found
    """
    if not n_iter: n_iter = round(10e20)
    seen = {start_pattern}
    current = start_pattern
    for i in range(1,n_iter):
        current = function(current)
        # print(current)
        if current in seen:
            print('found at step',i,current)
            return i,current
        seen.add(current)

# Cell
def find_cycle(start_pattern, function):
    """
        Find cycle length of some repeating pattern, by first inspecting which item repeats when
        And subtracting the time the item was first seen
    """
    step_second, pattern = find_repeat(start_pattern, function)
    step_first, pattern = find_pattern_in_iter(pattern, Test_gen(), goal = pattern)
    return step_second - step_first

# Cell
def factors(n):
    """
     return set of divisors of a number
    """

    step = 2 if n%2 else 1
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(sqrt(n))+1, step) if n % i == 0)))
