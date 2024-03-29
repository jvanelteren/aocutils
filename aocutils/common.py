# AUTOGENERATED! DO NOT EDIT! File to edit: ../00_common.ipynb.

# %% auto 0
__all__ = ['cat', 'chainit', 'copy_func', 'patch_to', 'patch', 'to_int', 'ints', 'flatten', 'zippify', 'multidict', 'rev', 'data',
           'quantify', 'atom', 'atoms', 'list_atoms', 'list_multiply', 'mapt']

# %% ../00_common.ipynb 2
from collections.abc import Iterable
from collections import namedtuple, deque, defaultdict
from itertools   import chain, combinations, permutations
import string
import re
from typing import Union
import numpy as np
from functools import partial
import functools
from types import FunctionType

# %% ../00_common.ipynb 3
def copy_func(f):
    "Copy a non-builtin function (NB `copy.copy` does not work for this)"
    if not isinstance(f,FunctionType): return copy(f)
    fn = FunctionType(f.__code__, f.__globals__, f.__name__, f.__defaults__, f.__closure__)
    fn.__dict__.update(f.__dict__)
    return fn

def patch_to(cls, as_prop=False):
    "Decorator: add `f` to `cls`"
    if not isinstance(cls, (tuple,list)): cls=(cls,)
    def _inner(f):
        for c_ in cls:
            nf = copy_func(f)
            # `functools.update_wrapper` when passing patched function to `Pipeline`, so we do it manually
            for o in functools.WRAPPER_ASSIGNMENTS: setattr(nf, o, getattr(f,o))
            nf.__qualname__ = f"{c_.__name__}.{f.__name__}"
            setattr(c_, f.__name__, property(nf) if as_prop else nf)
        return f
    return _inner

def patch(f):
    "Decorator: add `f` to the first parameter's class (based on f's type annotations)"
    cls = next(iter(f.__annotations__.values()))
    return patch_to(cls)(f)

# %% ../00_common.ipynb 6
def to_int(
    it: Iterable,    # watch out because passing a string '12t' will be ripped into a list [1,2,t]
    intonly=False):  # removes non-ints if set to True
    """
    Returns contents of iterable converted to int if possible
    
    Examples
    --------
    >>> to_int(['-12', 2, 'a'])
    [-12, 2, 'a']
    """

    if not it:
        print('empty line, returning []')
        return []
    if isinstance(it,str):
        print('watch out string will be converted into list with string.split()')
        it = it.split()
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

# %% ../00_common.ipynb 8
def ints(text: str, tolist=False) -> tuple[int]:
    """
    Return a tuple of all the integers in a string, discards everything else
    """
    return tuple(map(int, re.findall('-?[0-9]+', text))) if not tolist else list(map(int, re.findall('-?[0-9]+', text)))

# %% ../00_common.ipynb 10
def flatten(x:Iterable):
    def _flatten(x):
        for item in x:
            if isinstance(item,Iterable) and not isinstance(item, str):
                yield from _flatten(item)
            else:
                yield item
    """ 
    recursive flattens the input. Returns a list
    """
    return list(_flatten(x))



# %% ../00_common.ipynb 12
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

# %% ../00_common.ipynb 14
def multidict(items: Iterable[tuple], both=False) -> dict:
    "Given (key, val) pairs, return {key: [val, ....], ...}."
    result = defaultdict(list)
    for key, val in items:
        result[key].append(val)
        if both:
            result[val].append(key)
    return result

# %% ../00_common.ipynb 16
def rev(d:dict) -> dict:
    "Reverses keys and values. Make sure the value is hashable"
    return {v:k for k,v in d.items()}

# %% ../00_common.ipynb 19
def data(filename='input', parser=str, sep='\n') -> list:
    "Split the day's input file into sections separated by `sep`, and apply `parser` to each."
    sections = open(f'{filename}.txt').read().rstrip().split(sep)
    return [parser(section) for section in sections]

# %% ../00_common.ipynb 20
def quantify(iterable, pred=bool) -> int:
    "Count the number of items in iterable for which pred is true."
    return sum(1 for item in iterable if pred(item))

# %% ../00_common.ipynb 22
def atom(text: str) -> Union[float, int, str]:
    "Parse text into a single float or int or str."
    try:
        val = float(text)
        return round(val) if round(val) == val else val
    except ValueError:
        return text


# %% ../00_common.ipynb 24
def atoms(text: str, ignore=r'', sep=None) -> tuple[Union[int, str]]:
    "Parse text into atoms (numbers or strs), possibly ignoring a regex."
    if ignore:
        text = re.sub(ignore, '', text)
    return tuple(map(atom, text.split(sep)))


# %% ../00_common.ipynb 26
def list_atoms(inp: list):
    return tuple(map(atom, inp))


# %% ../00_common.ipynb 28
def list_multiply(a:Iterable,b:Iterable)->list:
    """
        Multiplies two iterables elementwise

        list_multiply([1,2,3],[2,3,4]) -> [2, 6, 12]
    """
    return (np.array(a)*np.array(b)).tolist()


# %% ../00_common.ipynb 30
def mapt(fn, *args):
    "map(fn, *args) and return the result as a tuple."
    return tuple(map(fn, *args))
mapt(lambda x: x+'z', list('abcde'))

# %% ../00_common.ipynb 31
cat = ''.join
chainit = chain.from_iterable
