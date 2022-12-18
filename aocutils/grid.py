# AUTOGENERATED! DO NOT EDIT! File to edit: ../01_grid.ipynb.

# %% auto 0
__all__ = ['Dim', 'gridneigh', 'arr_to_dict', 'grid_to_dict', 'neighbors', 'arr_neighbors', 'iterate', 'dimensions', 'positive',
           'manhattan', 'conv1d', 'conv2d', 'rotate']

# %% ../01_grid.ipynb 2
from collections import namedtuple
import numpy as np

# %% ../01_grid.ipynb 3
def gridneigh(filename, to_dict = True, diag=False, inc_self=False, parser=None):
    """
    Example to parse a simple grid consisting of ints
    When parser is None, characters will be parsed
    --------
    >>> grid, neigh = gridneigh('input.txt', parser=lambda x: [int(ch) for ch in x.split(',')])
    """

    if not parser:
        arr = [list(line) for line in open(filename, 'r').read().split('\n')]
    else:
        arr = [parser(line) for line in open(filename, 'r').read().split('\n')]
    neigh = arr_neighbors(arr,diag, inc_self)
    if to_dict:
        arr = arr_to_dict(arr)
    return arr, neigh
    
    

# %% ../01_grid.ipynb 4
def arr_to_dict(arr) -> dict: # numpy array or list of lists (tuple of tuples) 
    """ 
    Example
    --------
    >>>arr_to_dict([['a','b'],['c','#']])
    {(0, 0): 'a', (0, 1): 'b', (1, 0): 'c', (1, 1): '#'}
    """
    d = {}
    if isinstance(arr, str):
        raise TypeError("only works with list of lists or np.ndarray. Use grid_to_dict if input is a string grid")
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            d[(i,j)] = arr[i][j]
    return d


# %% ../01_grid.ipynb 6
def grid_to_dict(grid):
    if isinstance(grid, str):
        grid = [list(line) for line in grid.split('\n')]
    return arr_to_dict(grid)
    # return {(r,c): val for r, row in enumerate(grid) for c, val in enumerate(row)}
grid_to_dict([[1,2,3]])

# %% ../01_grid.ipynb 8
def neighbors(i, diag = False,inc_self=False):
    """
     determine the neighbors, returns a set with neighboring tuples {(0,1)}
     if inc_self: returns self in results
     if diag: return diagonal moves as well
    """
    r = [-1,0,1]
    c = [-1,0,1]
    if diag:
        if inc_self: 
            return {(i[0]+dr, i[1]+dc) for dr in r for dc in c}
        else: 
            return {(i[0]+dr, i[1]+dc) for dr in r for dc in c if not (dr == 0 and dc == 0)}
    else:
        res =  {(i[0],i[1]+1), (i[0],i[1]-1),(i[0]+1,i[1]),(i[0]-1,i[1])}
        if inc_self: res.add(i)
        return res

# %% ../01_grid.ipynb 10
def arr_neighbors(arr, diag=False, inc_self=False):
    """
    Returns a dictionary with index: set of neighbor indices
    Parameters: diag to include diagonal neighbors, inc_self to include self in result list
    Usage: for index, neighbor_indices in aoc.arr_neighbors(arr).items():
    """
    if not isinstance(arr, np.ndarray):
        arr = np.array(arr)
    res = {}
    for i in np.ndindex(arr.shape):
        # print('hi',i, neighbors(i,diag))
        res[i] = {(x,y) for x,y in neighbors(i,diag, inc_self) if 0<=x<arr.shape[0] and 0<=y<arr.shape[1]}
    return res


# %% ../01_grid.ipynb 13
def iterate(grid):
    for i,row in enumerate(grid):
        for j,val in enumerate(row):
            yield i,j,val

# %% ../01_grid.ipynb 14
Dim = namedtuple('Dim',['min','max','range'])
def dimensions(obj, axis=0): 
    """
     takes an iterable of iterables and returns a namedtuple with minima, maxima and range
     for example a 2d numpy array
     dim.min, dim.max and dim.range
    """
    if not isinstance(obj, np.ndarray):
        obj = np.array(list(obj).copy())

    minn = tuple(obj.min(axis = axis))
    maxx = tuple(obj.max(axis = axis))
    ranges = tuple(obj.ptp(axis=axis))
    
    res = Dim(minn, maxx, ranges)
    return res

# %% ../01_grid.ipynb 16
def positive(*args): 
    """ 
        takes 1 or multiple lists of n coordinates and returns it normalized (getting rid of negatives)
        Only works along rows! (axis=0)
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

# %% ../01_grid.ipynb 19
def manhattan(a,b):
    # n dimensional manhattan
    return sum(abs(x-y) for x,y in zip(a,b))

# %% ../01_grid.ipynb 21
def conv1d(arr,conv_shape,mode='same',padding=None,pad_dir='center') ->list:
    """
    Returns a list of kernel views of a string or list 
    mode == 'valid': returns only results where the kernel fits
    mode == 'same': return the same amount of items as original
    when mode =='same', default padding is the outer value
    """
    print('not fully checked yet', mode)
    
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


# %% ../01_grid.ipynb 23
def conv2d(arr,conv_shape,mode='valid',padding=None,pad_dir='center') ->list:
    """
    Returns a list of kernel views of a string or list 
    mode == 'valid': returns only results where the kernel fits
    mode == 'same': return the same amount of items as original
    when mode =='same', default padding is the outer value
    """
    print('not fully checked yet')
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


# %% ../01_grid.ipynb 25
def rotate(locs, flip=False):
    """
        Rotates a given pattern by 90 degrees (like a puzzle piece)
        when flip=True, also piece around leading to maximum of 8 options
    """
    def normalize(locs):
        minr = min(r for r,c in locs)
        minc = min(c for r,c in locs)
        return {(r-minr, c-minc) for r,c in locs}

    options = [{(r,c) for r,c in locs},
            {(c,-r) for r,c in locs},
            {(-r,-c) for r,c in locs},
            {(-c,r) for r,c in locs},
    ]
    if flip:
        options += [
            {(-r,c) for r,c in locs},
            {(c,r) for r,c in locs},
            {(r,-c) for r,c in locs},
            {(-c,-r) for r,c in locs}]
    return [normalize(o) for o in options]
    

