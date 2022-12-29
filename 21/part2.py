import ast
from copy import copy
import math
import pathlib
monkeys = pathlib.Path("21/input.txt").read_text().splitlines()

monkeys_dict = {}

class Monkey :
    
    def __init__(self, name : str) -> None:
        self.name = name
    
    def get_value(self):
        raise NotImplementedError
    
    def reset_value(self):
        raise NotImplementedError

class YellMonkey(Monkey):
    
    def __init__(self, name : str, value : int) -> None:
    
        super().__init__(name)
    
        self.yell_value = value
    
    def get_value(self):
        return self.yell_value

    def get_math_expression(self):
        
        if self.name == "humn":
            return "x"
        
        return f"{self.yell_value}"

    def set_value(self, value : int):
        self.yell_value = value
        

class MathMonkey(Monkey):
    
    def __init__(self,name : str,  all_monkeys_dict : dict,left_monkey : str, operation : str ,right_monkey : str) -> None:
    
        super().__init__(name)
    
        self.all_monkeys_dict = all_monkeys_dict
        self.left_monkey = left_monkey
        self.right_monkey = right_monkey
        
        self.operation_str = operation
        
        self.value = 0
        self.knows_value = False
        
        match operation:
            case "+" :
                self.operation = lambda x,y : x + y
            case "-" :
                self.operation = lambda x,y : x - y
            case "*" :
                self.operation = lambda x,y : x * y
            case "/" :
                self.operation = lambda x,y : int(x / y)
                
                
    def get_value(self):
        
        if self.knows_value:
            return self.value
        
        left_value = self.all_monkeys_dict[self.left_monkey].get_value()
        right_value = self.all_monkeys_dict[self.right_monkey].get_value()
        
        self.value = self.operation(left_value, right_value)
        self.knows_value = True
        
        return self.value
      
    def get_math_expression(self):
        
        left_expression = self.all_monkeys_dict[self.left_monkey].get_math_expression()
        right_expression = self.all_monkeys_dict[self.right_monkey].get_math_expression()
        
        return f"({left_expression}{self.operation_str}{right_expression})"
      
      
class RootMonkey:
    
    def __init__(self,name : str,  all_monkeys_dict : dict, left_monkey : str, right_monkey : str) -> None:
    
    
        self.all_monkeys_dict = all_monkeys_dict
        self.left_monkey = left_monkey
        self.right_monkey = right_monkey

    def compare_monkeys(self):

        left_value = self.all_monkeys_dict[self.left_monkey].get_value()
        right_value = self.all_monkeys_dict[self.right_monkey].get_value()

        return left_value - right_value

    def get_math_expression(self):
        
        left_expression = self.all_monkeys_dict[self.left_monkey].get_math_expression()
        right_expression = self.all_monkeys_dict[self.right_monkey].get_math_expression()
        
        return f"{left_expression}=={right_expression}"

for monkey in monkeys:
    
    name = monkey.split(":")[0]

    number = monkey.split(":")[1][1:]

    if any(operation in number for operation in ("+", "*", "-", "/")):

        left_monkey = number.split(" ")[0]
        operation = number.split(" ")[1]
        right_monkey = number.split(" ")[2]
        
        if name == "root":
            monkeys_dict[name] = RootMonkey(name,monkeys_dict, left_monkey,right_monkey)
        else:
            monkeys_dict[name] = MathMonkey(name,monkeys_dict, left_monkey, operation, right_monkey)
        
    else:
        monkeys_dict[name] = YellMonkey(name, int(number))
        


math_expression = monkeys_dict["root"].get_math_expression()
    
#print(math_expression)

# Is using sympy cheating?

from sympy.parsing.sympy_parser import parse_expr, standard_transformations
from sympy import Symbol
from sympy.solvers import solve
x = Symbol('x')
left_expression = parse_expr(math_expression.split("==")[0], transformations=standard_transformations)
right_expression = parse_expr(math_expression.split("==")[1], transformations=standard_transformations) 

humn_value = solve(left_expression - right_expression, x)[0]

print(humn_value)