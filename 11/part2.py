from copy import copy, deepcopy
import math
from typing import Callable


class Monkey:
    
    def __init__(self, starting_items : list, operation_str : str, devisor : int, sucess_monkey : int, fail_monkey : int) -> None:
        
        self.items = copy(starting_items)
        if operation_str == "* old":
            self.operation = lambda x: x**2
        elif operation_str.startswith("+"):
            self.operation = lambda x: x + int(operation_str[1:])
        elif operation_str.startswith("-"):
            self.operation = lambda x: x - int(operation_str[1:])
        elif operation_str.startswith("*"):
            self.operation = lambda x: x * int(operation_str[1:])
        self.devisor = devisor
        self.sucess_monkey = sucess_monkey
        self.fail_monkey = fail_monkey
        self.inspections = 0
        self.lcm = 1
        
    def inspect(self) -> None:
        if len(self.items)!= 0:
            self.items[0] = self.operation(self.items[0])
            self.inspections += 1
            
    def test(self) -> tuple[int, int]:
        target = self.sucess_monkey if self.items[0] % self.devisor == 0 else self.fail_monkey
        item = self.items.pop(0) % self.lcm
        
        return target, item
    
    def recieve(self, item : int) -> None:
        self.items.append(item)
        
import pathlib
data = pathlib.Path("11/input.txt").read_text()
lines = data.splitlines()

monkeys : list[Monkey]= []

for line_index in range(0, len(lines), 7):
    starting_items = list(map(int,lines[line_index+1].split("items:")[1].split(",")))
    
    operation_str = lines[line_index+2].split("new = old")[1].strip()
    
    
        
    devisor = int(lines[line_index+3].split("divisible by")[1].strip())
    success_monkey = int(lines[line_index+4].split("If true: throw to monkey")[1].strip())
    fail_monkey = int(lines[line_index+5].split("If false: throw to monkey")[1].strip())
    
    monkey = Monkey(starting_items, operation_str, devisor, success_monkey, fail_monkey)
    
    monkeys.append(monkey)
    
devisors = [monkey.devisor for monkey in monkeys]
lcm = math.lcm(*devisors)
for monkey in monkeys:
    monkey.lcm = lcm
    
DEBUG = False
for _ in range(10000):
    
    for monkey in monkeys:
        while len(monkey.items) != 0:    
            monkey.inspect()
            monkey_index, item = monkey.test()
            monkeys[monkey_index].recieve(item)
        if DEBUG:
            for monkey_t in monkeys:
                print(monkey_t.items)
            print()
inspections = sorted([monkey.inspections for monkey in monkeys], reverse=True)
print(inspections[0]*inspections[1])