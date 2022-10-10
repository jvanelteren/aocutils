# AUTOGENERATED! DO NOT EDIT! File to edit: ../00_common.ipynb.

# %% auto 0
__all__ = ['cat', 'flatten', 'to_int', 'ints', 'rev', 'zippify', 'list_multiply', 'data', 'quantify', 'first', 'multimap', 'atom',
           'atoms', 'list_atoms', 'dotproduct', 'mapt']

# %% ../00_common.ipynb 2
from collections.abc import Iterable
from collections import namedtuple, deque, defaultdict
from itertools   import chain, combinations, permutations
import string
import re
from typing import Union
import numpy as np
from functools import partial

# %% ../00_common.ipynb 3
def to_int(
    it: Iterable,   # watch out because passing a string '12t' will be ripped into a list [1,2,t]
    intonly=False):  # removes non-ints if set to True
    """
    returns items converted to int if possible
    
    Examples
    --------
    >>> to_int(['-12', 2, 'a'])
    [-12, 2, 'a']
    """

    if not it:
        print('empty line, returning []')
        return []
    if isinstance(it,str):
        print('watch out string will be converted into list of characters and single digit ints')
    if isinstance(it[0],list):
        return list(to_int(l) for l in it)
    if isinstance(it[0],tuple):
        return tuple(to_int(l) for l in it)

    out = []
    for i in it:
        try:
            out.append(int(i))
        except ValueError:
            if not intonly:
                out.append(i)
    if isinstance(it,tuple): return tuple(out)
    else: return list(out)

# %% ../00_common.ipynb 5
def ints(text: str) -> tuple[int]:
    """
    Return a tuple of all the integers in a string, discards everything else
    """
    return tuple(map(int, re.findall('-?[0-9]+', text)))

# %% ../00_common.ipynb 7
def flatten(x:Iterable):
    """ 
    recursive flattens the input. Returns a list
    """
    return list(_flatten(x))

def _flatten(x):
    for item in x:
        if isinstance(item,Iterable) and not isinstance(item, str):
            yield from _flatten(item)
        else:
            yield item

# %% ../00_common.ipynb 9
def rev(d:dict) -> dict:
    "Reverses keys and values"
    return {v:k for k,v in d.items()}

# %% ../00_common.ipynb 11
def zippify(iterable, len=2, cat=False):
    """
        Zips an iterable with arbitrary length pieces
        
        e.g. to create a moving window with len n
        
        Example:
        zippify('abcd',2, cat=False)
        --> [('a', 'b'), ('b', 'c'), ('c', 'd')]

        If cat = True, joins the moving windows together
        zippify('abcd',2, cat=True)
        --> ['ab', 'bc', 'cd']
    """
    iterable_collection = [iterable[i:] for i in range(len)]
    res = list(zip(*iterable_collection))
    return [''.join(r) for r in res] if cat else res

# %% ../00_common.ipynb 13
def list_multiply(a:Iterable,b:Iterable)->list:
    """
        Multiplies two iterables elementwise

        list_multiply([1,2,3],[2,3,4]) -> [2, 6, 12]
    """
    return (np.array(a)*np.array(b)).tolist()


# %% ../00_common.ipynb 16
def data(filename='input', parser=str, sep='\n') -> list:
    "Split the day's input file into sections separated by `sep`, and apply `parser` to each."
    sections = open(f'{filename}.txt').read().rstrip().split(sep)
    return [parser(section) for section in sections]

# %% ../00_common.ipynb 17
def quantify(iterable, pred=bool) -> int:
    "Count the number of items in iterable for which pred is true."
    return sum(1 for item in iterable if pred(item))

# %% ../00_common.ipynb 19
def first(iterable, default=None) -> object:
    "Return first item in iterable, or default."
    return next(iter(iterable), default)

# %% ../00_common.ipynb 21
def multimap(items: Iterable[tuple]) -> dict:
    "Given (key, val) pairs, return {key: [val, ....], ...}."
    result = defaultdict(list)
    for key, val in items:
        result[key].append(val)
    return result

# %% ../00_common.ipynb 23
def atom(text: str) -> Union[float, int, str]:
    "Parse text into a single float or int or str."

    try:
        val = float(text)
        return round(val) if round(val) == val else val
    except ValueError:
        return text
atom('11') == 11


# %% ../00_common.ipynb 24
def atoms(text: str, ignore=r'', sep=None) -> tuple[Union[int, str]]:
    "Parse text into atoms (numbers or strs), possibly ignoring a regex."
    if ignore:
        text = re.sub(ignore, '', text)
    return tuple(map(atom, text.split(sep)))
atoms('abc 111 def')

# %% ../00_common.ipynb 25
def list_atoms(inp: list):
    return tuple(map(atom, inp))


# %% ../00_common.ipynb 27
def dotproduct(A, B) -> float: return sum(a * b for a, b in zip(A, B))
dotproduct([1,2],[7,8]) == 23

# %% ../00_common.ipynb 28
def mapt(fn, *args):
    "map(fn, *args) and return the result as a tuple."
    return tuple(map(fn, *args))
mapt(lambda x: x+'z', list('abcde'))

# %% ../00_common.ipynb 29
cat = ''.join
flatten = chain.from_iterable
