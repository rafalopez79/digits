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
    print('Usage digits.py objective d1 d2 d3 d4 d5 d6')

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

def distance(a:int, b: int):
    return abs(a-b)

def compute_step(a: int, op: str, b: int, queue: List, obj: int, nums: List[int], prev_steps: List[Step]):
    result = operate(a, b, op)
    if result is not None:
        remaining = list(nums)
        if a in remaining:
            remaining.remove(a)
        if b in remaining:
            remaining.remove(b)
        step = Step(a, op, b, result, remaining)
        solution = Solution(prev_steps+[step])
        val = distance(obj, result)
        heapq.heappush(queue, (val, solution))

def compute(obj: int, nums: List[int]) -> Solution|None:
    operators = ['+','-','*','/']
    queue = []
    pairs = [(x,y) for i,x in enumerate(nums) for j,y in enumerate(nums) if i != j]
    #genero heap
    for p in pairs:
        for op in operators:
            a = p[0]
            b = p[1]
            compute_step(a, op, b, queue, obj, nums, [])
    best = None
    bestDistance = None
    while len(queue) > 0:
        item = heapq.heappop(queue)
        prev = item[1].steps
        last_step :Step|None = last(prev)
        if last_step is not None:
            result = last_step.result
            dist = distance(result, obj)
            if bestDistance is None or dist < obj:
                best = item[1]
                bestDistance = dist
            if result == obj:
                return item[1]
            else:
                remaining = last_step.remaining
                for b in remaining:
                    for op in operators:
                        compute_step(result, op, b, queue, obj, remaining, prev)
                        compute_step(b, op, result, queue, obj, remaining, prev)
    return best

def main():
    if len(sys.argv) != 8:
        print_usage()
        return
    objective=num(sys.argv[1])
    digits = [num(i) for i in sys.argv[2:8]]
    if objective is None or None in digits:
        print_usage()
        return
    solution = compute(objective, [i for i in digits if i is not None])
    if solution is not None:
        for step in solution.steps:
            print('{} {} {} = {}'.format(step.a, step.op, step.b, step.result))
    else:
        print('Not found')
    

if __name__ == "__main__":
    main()
