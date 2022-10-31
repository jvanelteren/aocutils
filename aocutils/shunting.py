# AUTOGENERATED! DO NOT EDIT! File to edit: ../07_shunting_yard.ipynb.

# %% auto 0
__all__ = ['ShuntingYard']

# %% ../07_shunting_yard.ipynb 1
import math
from collections import deque
from collections import defaultdict
import operator

left_associative = {'-', '/', '+', '*'}


# %% ../07_shunting_yard.ipynb 2
# https://en.wikipedia.org/wiki/Associative_property
# https://en.wikipedia.org/wiki/Shunting-yard_algorithm
# https://adventofcode.com/2020/day/18
class ShuntingYard:
    """
    Init with a precedence dictionary. Then call SY.calc(line), with a string as input
    
    Example precedence dictionary. Higher numbers have a higher precedence:
    prec = defaultdict(lambda: int(9))
    prec.update({'*':4, 
            '+':4,
            '/':4, 
            ':':4,
            '-':4,
            '^':4,
            '**':4})
    
    self.ops is a dictionary with the functions that are called with certain symbols, e.g.
    Example self.ops:
    self.ops = {
            '+' : operator.add,
            '-' : operator.sub,
            '*' : operator.mul,
            '/' : operator.truediv,  
            ':' : operator.truediv,
            '%' : operator.mod,
            '^' : operator.xor,
            '**' : pow,
        }

    
    """
    def __init__(self, prec=None, ops=None):
        self.prec = {
            '**':7, 
            '/':6, 
            '*':6, 
            ':':6,
            '+':5,
            '-':5,
            '<<':4,
            '>>': 4,
            '&': 3,
            '^':2,
            '|': 1} if not prec else prec
    
        self.ops = {
            '+' : operator.add,
            '-' : operator.sub,
            '*' : operator.mul,
            '/' : operator.truediv,  
            ':' : operator.truediv,
            '%' : operator.mod,
            '^' : operator.xor,
            '**' : pow,
        } if not ops else ops

    def is_callable_string(self, s):
        try:
            res = eval(f'callable({s})')
        except Exception:
            return False
        return True

    def get_postfix(self, list_of_symbols):
        op_stack = deque()
        output_stack = deque()

        for symbol in list_of_symbols:
            # print(output_stack, op_stack)
            if isinstance(symbol, int): 
                output_stack.append(symbol)
            elif self.is_callable_string(symbol): 
                op_stack.append(symbol)
            elif symbol in self.prec:
                while (op_stack and op_stack[-1] != '(' and (
                    self.prec[op_stack[-1]] > self.prec[symbol] or 
                    (self.prec[op_stack[-1]] == self.prec[symbol] and symbol in '-/*+'))):
                    output_stack.append(op_stack.pop())
                op_stack.append(symbol)
            
            elif symbol == '(': op_stack.append(symbol)
            elif symbol == ')': 
                while op_stack[-1] != '(':
                    output_stack.append(op_stack.pop())
                if op_stack and op_stack[-1]=='(':
                    op_stack.pop() # remove the (
                if op_stack and callable(op_stack[-1]):
                    output_stack.append(op_stack.pop())
        while op_stack:
            output_stack.append(op_stack.pop())
        
        return output_stack

    def eval_postfix(self, output_stack):
        res = []
        for symbol in output_stack:
            if isinstance(symbol, int): res.append(symbol)
            else:
                second, first = res.pop(), res.pop()
                if symbol in self.ops:
                    temp = self.ops[symbol](first, second)
                else:
                    temp = eval(f'{symbol}({first},{second})')
                res.append(temp)
        return res[0]
    
    def calc(self, line):
        line = line.replace("(","( ").replace(")"," )")
        line = [int(arg) if arg.isnumeric() else arg for arg in line.split()]
        return self.eval_postfix(self.get_postfix(line))
