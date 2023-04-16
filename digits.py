#!/usr/bin/env python3
import sys, heapq
from typing import Tuple, List, TypeVar
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class Step:
    """Class for keeping track computing steps."""
    a: int
    op:str
    b: int
    result:    int
    remaining: List[int]

@dataclass
class Solution:
    """Partial solution"""
    steps: List[Step]
    
    def __lt__(self, other):
        return len(self.steps) < len(other.steps)

def num(s: str) -> int|None:
    """int parser"""
    try:
        return int(s)
    except ValueError:
        return None

def print_usage():
    print('Usage digits.py objective d1 d2 ...')

def operate(a: int, b: int, op: str) -> int|None:
    if op == '+':
        return a+b
    elif op == '*':
        return a*b
    elif op == '-':
        if a - b > 0:
            return a - b
        else:
            return None
    elif op == '/':
        if b > 0 and a % b == 0:
            return a // b
        else: 
            return None

def last(l:List[T]) -> T|None:
    if len(l) == 0:
        return None
    else:
        return l[-1]

def distance(obj:int, values: List[int]):
    """distance between the nearest element of values and obj"""
    if len(values) == 0:
        return 0
    d = 0
    for v in values:
        dist = abs(obj - v)
        if dist < d:
            d = dist
    return d

def compute_step(a: int, op: str, b: int, queue: List, obj: int, nums: List[int], prev_steps: List[Step]):
    result = operate(a, b, op)
    if result is not None:
        remaining = list(nums)
        if a in remaining:
            remaining.remove(a)
        if b in remaining:
            remaining.remove(b)
        nremaining = [] + remaining + [result]
        step = Step(a, op, b, result, nremaining)
        solution = Solution(prev_steps+[step])
        val = distance(obj, nremaining)
        heapq.heappush(queue, (val, solution))

def get_ops(nums: List[int]) -> List[Tuple[int,str,int]]:
    operators = ['+','-','*','/']
    commutative_operators = ['+','*']
    result = set()
    used = set()
    for op in operators:
        commutative = op in commutative_operators
        for i,x in enumerate(nums):
            for j,y in enumerate(nums):
                if i != j:
                    e = (x, op, y)
                    r = (y, op, x)
                    if commutative and e not in used and r not in used:
                        used.add(e)
                        used.add(r)
                        result.add(e)
                    elif not commutative and e not in used:
                        used.add(e)
                        result.add(e)
    return list(result)

def compute(obj: int, nums: List[int]) -> Solution|None:
    queue = []
    ops = get_ops(nums)
    #genero heap
    for p in ops:
        compute_step(p[0], p[1], p[2], queue, obj, nums, [])
    best = None
    bestDistance = None
    while len(queue) > 0:
        item = heapq.heappop(queue)
        prev = item[1].steps
        last_step :Step|None = last(prev)
        if last_step is not None:
            remaining = last_step.remaining
            if obj in remaining:
                return item[1]
            if len(remaining) == 1:
                d = abs(obj-remaining[0])
                if bestDistance is None or d < bestDistance:
                    bestDistance = d
                    best = item[1]
            else:
                remaining = last_step.remaining
                ops = get_ops(remaining)
                for p in ops:
                    compute_step(p[0], p[1], p[2], queue, obj, remaining, prev)
    return best

def main():
    if len(sys.argv) <= 2:
        print_usage()
        return
    objective=num(sys.argv[1])
    digits = [num(i) for i in sys.argv[2:]]
    if objective is None or None in digits:
        print_usage()
        return
    solution = compute(objective, [i for i in digits if i is not None])
    if solution is not None:
        found = False
        for step in solution.steps:
            print('{} {} {} = {}'.format(step.a, step.op, step.b, step.result))
            if step.result == objective:
                found = True
                print('Exact match!')
        if not found:
            print('Best approach!')
    else:
        print('Not found')
    

if __name__ == "__main__":
    main()
