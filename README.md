aocutils
================

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

This file will become your README and also the index of your
documentation!

## Install

``` sh
pip install -e .
```

This installs locally and refreshes changes to the codebase
automatically

## How to use

Import the functions from the submodules

``` python
from aocutils.grid import arr_to_dict
arr_to_dict([('a', 1), ('b',5)])
```

    {(0, 0): 'a', (0, 1): 1, (1, 0): 'b', (1, 1): 5}

These are all the imports that could come in handy for AoC

from bisect import bisect_left from collections import namedtuple,
deque, defaultdict from functools import reduce import heapq from
itertools import chain from math import sqrt, gcd, comb import operator
import re import string

import networkx as nx import numpy as np import pandas as pd

    from aocutils.common import copy_func, patch_to, patch, to_int, ints, flatten, zippify, multidict, rev, data, quantify, atom, atoms, list_atoms, list_multiply, mapt
    from aocutils.grid import gridneigh, arr_to_dict, grid_to_dict, neighbors, arr_neighbors, iterate, Dim, dimensions, positive, manhattan, conv1d, conv2d, rotate
    from aocutils.maze import graphparse, bfs, dijkstra, get_path, dfs
    from aocutils.math import gcd, factors, lcm, crt, mul_inv, Segment, lis, angle, all_combinations, all_permutations, mst
    from aocutils.special import md5, binarysearch, deduce_matches, find_specific_pattern, find_repeat, find_cycle, UnionFind, Octree, LazySegmentTree, Trie
    from aocutils.visuals import visualize_graph, labelize, animate_grid, plot
    from aocutils.cfg import CFG
    from aocutils.earley import State, Earley
    from aocutils.shunting import ShuntingYard

And links to useful docs:

[Docs on aocutils](https://jvanelteren.github.io/aocutils/)

[Docs on nbdev](https://nbdev.fast.ai/explanations/directives.html)
