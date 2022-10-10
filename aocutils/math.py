# AUTOGENERATED! DO NOT EDIT! File to edit: ../03_math.ipynb.

# %% auto 0
__all__ = ['factors', 'gcd', 'lcm', 'crt', 'mul_inv', 'lis', 'all_combinations', 'all_permutations']

# %% ../03_math.ipynb 2
from functools import reduce
from math import sqrt, gcd, comb
from bisect import bisect_left
from itertools import combinations, permutations

# %% ../03_math.ipynb 3
def factors(n):
    """
     return set of divisors of a number
    """
    step = 2 if n % 2 else 1
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(sqrt(n))+1, step) if n % i == 0)))


# %% ../03_math.ipynb 5
def gcd(a,b):
    largest = max(a,b)
    smallest = min(a,b)
    if a == b: 
        return a
    if not largest % smallest:
        return smallest
    while True:
        rest = largest % smallest
        if rest == 0:
            return prevrest
        else:
            prevrest = rest
            largest = smallest
            smallest = rest

def lcm(a):
    lcm = a[0]
    for i in a[1:]:
        lcm = lcm*i//gcd(lcm, i)
    return lcm



# %% ../03_math.ipynb 8
def crt(remainders, moduli):
    """
        Chinese remainder theorem
    """
    cur_rem = remainders[0]
    cur_mod = moduli[0]
    for rem, mod in zip(remainders[1:], moduli[1:]):
        i = 0
        while True:
            if (cur_rem + i * cur_mod) % mod == rem % mod:
                cur_rem += i * cur_mod
                cur_mod = lcm((cur_mod, mod))
                break
            else:
                i+=1
    print('Returning remainder and modulo. First valid number is the remainder')
    return cur_rem, cur_mod

# %% ../03_math.ipynb 13
def mul_inv(a, b):
    # solves e.g. 40x === 1(mod 7) --> 3
    # since 40-35 --> 5x === 1mod(7), if x would be 3, 15 === 1 (mod 7)
    # this is called the multiplicative inverse
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

# %% ../03_math.ipynb 19
def lis(nums, increase=True):
    """
        Computes the length of the longest in(de)creasing subsequence
    """
    previous = [-1] * len(nums)
    current = []
    ans = []
    
    for i, num in enumerate(nums):
        idx = bisect_left(current, num)
        previous[i] = current[idx-1] if idx else -1
        if idx == len(current):
            current.append(num)
            ans.append(num)
        else:
            current[idx] = num
        print(current)
    
    return ans

    

# %% ../03_math.ipynb 23
def all_combinations(it, n = None):
    if not n:
        n = len(it) - 1
    for i in range(1,n + 1):
        for comb in combinations(it,i):
            yield comb

# %% ../03_math.ipynb 24
def all_permutations(it, n = None):
    if not n:
        n = len(it) - 1
    for i in range(1,n + 1):
        for perm in permutations(it,i):
            yield perm
