# AUTOGENERATED! DO NOT EDIT! File to edit: ../05_norvig.ipynb.

# %% auto 0
__all__ = ['cat', 'flatten', 'data', 'do', 'quantify', 'first', 'rest', 'multimap', 'atom', 'atoms', 'list_atoms', 'dotproduct',
           'mapt']

# %% ../05_norvig.ipynb 2
from collections import defaultdict
from itertools   import chain
import numpy as np
import re
from typing import Union
from functools import partial
import string


# %% ../05_norvig.ipynb 3
def data(filename='input', parser=str, sep='\n') -> list:
    "Split the day's input file into sections separated by `sep`, and apply `parser` to each."
    sections = open(f'{filename}.txt').read().rstrip().split(sep)
    return [parser(section) for section in sections]
     
def do(day, *answers) -> dict[int, int]:
    "E.g., do(3) returns {1: day3_1(in3), 2: day3_2(in3)}. Verifies `answers` if given."
    g = globals()
    got = []
    for part in (1, 2):
        fname = f'day{day}_{part}'
        if fname in g: 
            got.append(g[fname](g[f'in{day}']))
            if len(answers) >= part: 
                assert got[-1] == answers[part - 1], (
                    f'{fname}(in{day}) got {got[-1]}; expected {answers[part - 1]}')
    return got

# %% ../05_norvig.ipynb 4
def quantify(iterable, pred=bool) -> int:
    "Count the number of items in iterable for which pred is true."
    return sum(1 for item in iterable if pred(item))

# %% ../05_norvig.ipynb 6
def first(iterable, default=None) -> object:
    "Return first item in iterable, or default."
    return next(iter(iterable), default)

# %% ../05_norvig.ipynb 8
def rest(sequence) -> object: return sequence[1:]

# %% ../05_norvig.ipynb 10
from collections.abc import Iterable
def multimap(items: Iterable[tuple]) -> dict:
    "Given (key, val) pairs, return {key: [val, ....], ...}."
    result = defaultdict(list)
    for key, val in items:
        result[key].append(val)
    return result

# %% ../05_norvig.ipynb 12
def atom(text: str) -> Union[float, int, str]:
    "Parse text into a single float or int or str."

    try:
        val = float(text)
        return round(val) if round(val) == val else val
    except ValueError:
        return text
atom('11') == 11


# %% ../05_norvig.ipynb 13
def atoms(text: str, ignore=r'', sep=None) -> tuple[Union[int, str]]:
    "Parse text into atoms (numbers or strs), possibly ignoring a regex."
    if ignore:
        text = re.sub(ignore, '', text)
    return tuple(map(atom, text.split(sep)))
atoms('abc 111 def')

# %% ../05_norvig.ipynb 14
def list_atoms(inp: list):
    return tuple(map(atom, inp))


# %% ../05_norvig.ipynb 16
def dotproduct(A, B) -> float: return sum(a * b for a, b in zip(A, B))
dotproduct([1,2],[7,8]) == 23

# %% ../05_norvig.ipynb 17
def mapt(fn, *args):
    "map(fn, *args) and return the result as a tuple."
    return tuple(map(fn, *args))
mapt(lambda x: x+'z', list('abcde'))

# %% ../05_norvig.ipynb 18
cat = ''.join
flatten = chain.from_iterable