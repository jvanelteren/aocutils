# AUTOGENERATED! DO NOT EDIT! File to edit: ../06_context_free_grammar.ipynb.

# %% auto 0
__all__ = ['CFG']

# %% ../06_context_free_grammar.ipynb 2
from collections import defaultdict
from itertools import product

# %% ../06_context_free_grammar.ipynb 3
class CFG():
    """Takes a grammer as dict with tuple of options as values. Terminal values should not be in a tuple but as a string
    Usage:
        cfg = CFG(grammar_dict)
            reverse as optional parameter when k,v are reversed
            converts the grammar to Chomsky Normal form by taking care of options, unit productions and triplets
        cfg.solve(messages_list) returns dict of substrings with possible rules to make them
    """
    def __init__(self, grammar = None, reverse = True):
        self.outcomes = defaultdict(set)
        if grammar:
            # convert grammar to CNF and add terminals to outcomes
            self.grammar = self.grammar_to_cnf(grammar, reverse)
            self.outcomes.update({k:v for k,v in self.grammar.items() if isinstance(k, str)})


    def grammar_to_cnf(self, grammar, reverse):
        grammar = self.to_cnf_remove_options(grammar, reverse)
        grammar = self.to_cnf_remove_triplets(grammar)
        return self.to_cnf_remove_unit_productions(grammar)

    def to_cnf_remove_options(self, grammar, reverse):
        # if reverse change from X : AB to AB : {X}
        # if there are options, these are given a separate entry, e.g.
        # X : (AB, CD) --> X: AB and X: CD
        new_grammar = defaultdict(set)
        if reverse:
            for k,v in grammar.items():
                for option in v:
                    new_grammar[option].add(k)
        else:
            for k,v in grammar.items():
                for option in k:
                    new_grammar[option].add(v)
        return new_grammar
        
    def to_cnf_remove_triplets(self, grammar):
        # reduces triplets or larger to pairs
        # changes X : ABC to
        # X: AY, Y = BC
        new_grammar = defaultdict(set)
        for k,v in grammar.items():
            if len(k) > 2:
                for i, t in enumerate(k[0:-2]):
                    newvar = str(v) + '_' + str(i)
                    oldvar = str(v) + '_' + str(i-1)
                    if i == 0:
                        new_grammar[t,newvar] = v
                    else:
                        new_grammar[t,newvar] = {oldvar}
                new_grammar[k[-2:]].add(newvar)
            else:
                new_grammar[k] |= v
        return new_grammar
           
    
    def to_cnf_remove_unit_productions(self,grammar):
        # step to get to Chomsky Normal Form
        # if X : A, duplicate all A : Y with X : Y
        singulars = {k[0]:next(iter(v)) for k,v in grammar.items() if len(k)!=2 and not isinstance(k,str)}
        for k,v in singulars.items():
            for j in grammar.values():
                if k in j:
                    j.add(v)
        return grammar

    def pieces(self, test,l):
        # gets all possibilities of len l out of a string
        assert isinstance(test, str)
        return {test[i:i+l] for i in range(len(test)-l+1) if test[i:i+l] not in self.outcomes}

    def splitter(self,option):
        # splits string into all options of two substrings
        assert isinstance(option, str)
        return {(option[:i], option[i:]) for i in range(1,len(option))}

    def check_possible_option(self, option):
        first = self.outcomes[option[0]]
        second = self.outcomes[option[1]]
        res = set()
        for potential in product(first,second):
            if potential in self.grammar: res |= self.grammar[potential]
        return res

    def solve(self, messages):
        # takes a list of messages and returns all possibilities for the substrings of m
        for num, m in enumerate(messages):
            if num % 100 == 0: print(num*10, 'messages done')
            for i in range(2,len(m)+1):
                for j in self.pieces(m, i):
                    for k in self.splitter(j):
                        res = self.check_possible_option(k)
                        if res:
                            self.outcomes[j] |= res
        print('finished all messages, returning dict')
        return self.outcomes
          


