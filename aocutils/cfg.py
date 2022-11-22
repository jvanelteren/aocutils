# AUTOGENERATED! DO NOT EDIT! File to edit: ../07_earleyparser.ipynb.

# %% auto 0
__all__ = ['State', 'parse', 'find', 'printparse']

# %% ../07_earleyparser.ipynb 2
from pprint import pprint
from typing import NamedTuple
from functools import cache
from collections import deque


# %% ../07_earleyparser.ipynb 3
class State(NamedTuple):
    symbol: str
    rule: tuple
    startidx: int
    position: int
    predecessor: object
    creator: object
       
    def __repr__(self):
        pos = self.position
        return f"{self.symbol:<3}: {str(self.rule[:pos]):<15} | {str(self.rule[pos:]):<30} {'idx('}{self.startidx}) {'Done' if self.is_complete() else ''})"
    
    def is_complete(self):
        return self.position == len(self.rule)
    
    def nextsym(self):
        return False if self.is_complete() else self.rule[self.position]
    # def __eq__(self, other):
    #     return all(x==y for x, y in zip(self, other))
        

def parse(grammar, message, start, verbose=False, returncols = False):
    def scan(column, parsedsym, advancedstate):
        # we are scanning the states in a column to check if we can advance based on the parsed symbol
        advancedstates = []
        for state in column:
            if not state.is_complete() and state.nextsym() == parsedsym:
                symbol, rule, startidx, position, predecessor, creator = state
                position += 1
                advancedstates.append(State(symbol, rule, startidx, position, state, advancedstate))
        if verbose: print('parsed symbol:', message[colidx-1], ':we have advances on', [s['symbol'] for s in advancedstates])
        return advancedstates

    @cache
    def predict(colidx, symbol, advancedstate):
        seen = {symbol} # otherwise you can have infinite loop when recursively adding
        toadd = {(symbol, advancedstate)}
        predicted = set()
        while toadd:
            cur, curstate = toadd.pop()
            for rule in grammar.get(cur, []):
                newstate = State(cur, rule, colidx, 0, False, 'creator')
                predicted.add(newstate)
                if (recursivesymbol := newstate.rule[0]) not in seen:
                    toadd.add((recursivesymbol, newstate))
                    seen.add(recursivesymbol)
        return frozenset(predicted)
    
    def completer(cols, advancedstates):
        # check if any of the states are completed, if yes do scan again (loop untill nothing is completed)
        while advancedstates:
            advancedstate = advancedstates.pop()
            cols[colidx].add(advancedstate)
            if advancedstate.is_complete(): # do scan again, looking to advance other states based on the symbol of the completed rule
                if verbose: print('completion:', advancedstate['symbol'])
                advancedstates += scan(cols[advancedstate.startidx], advancedstate.symbol, advancedstate)
            else: # predict new states based on the next expected symbol in the rule
                cols[colidx] |= predict(colidx, advancedstate.nextsym(), advancedstate)

        
        
    def isvalid(cols):
        for state in cols[colidx]:
            if state.is_complete() and state.startidx == 0 and state.symbol == start:
                return True #('valid')
        else:
            return False

    def __init__():        
        cols = [set() for _ in range(len(message)+1)]
        cols[0] |= predict(0, start, 'starter')
        if verbose: pprint(cols[0])
        return cols
    
    #check input
    assert all(isinstance(v, tuple) for v in grammar.values()), 'a symbol should contain a tuple of 1 or more production rules'
    assert all(isinstance(option, tuple) for v in grammar.values() for option in v), 'rules in the grammar should be tuples'
    assert all(isinstance(ch, str) for v in grammar.values() for option in v for ch in option), 'symbols in the grammar should be strings'

    cols = __init__()
    for colidx in range(1, len(message)+1): # we just populated the 0th col, now the first character has colidx 1
        if verbose: print(colidx, message[colidx-1], len(cols[colidx-1]))
        advancedstates = scan(cols[colidx-1], message[colidx-1], 'scanner')
        completer(cols, advancedstates)
    return cols if returncols else isvalid(cols)

# %% ../07_earleyparser.ipynb 4
def find(cols, ans, endstate=False, start = False):
    if start:
        for state in cols[-1]:
            if state.is_complete() and state.startidx == 0 and state.symbol == '0':
                ans.appendleft(state)
    elif not isinstance(endstate, State):
        return ans
    else:
        ans.appendleft(endstate)
    cur = ans[0]          
    while isinstance(cur, State) and isinstance(cur.predecessor, State):
        if isinstance(cur, State):
            ans = find(cols, ans, cur.creator)
        ans.appendleft(cur.predecessor)
        cur = ans[0]
    
    return ans

def printparse(ans):
    # currently only print the begin of a rule and items descendents idented
    ident = -2
    prev = None
    for idx, state in enumerate(ans):
        if state.position == 0:
            ident += 2
            print('.'*ident, state)
        
        if state.is_complete():
            ident -= 2
        prev = state



