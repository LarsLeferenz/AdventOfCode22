import pathlib
monkeys = pathlib.Path("21/input.txt").read_text().splitlines()

monkeys_dict = {}

class Monkey :
    
    def __init__(self, name : str) -> None:
        self.name = name
    
    def get_value(self):
        raise NotImplementedError

class YellMonkey(Monkey):
    
    def __init__(self, name : str, value : int) -> None:
    
        super().__init__(name)
    
        self.yell_value = value
    
    def get_value(self):
        return self.yell_value

class MathMonkey(Monkey):
    
    def __init__(self,name : str,  all_monkeys_dict : dict,left_monkey : str, operation : str ,right_monkey : str) -> None:
    
        super().__init__(name)
    
        self.all_monkeys_dict = all_monkeys_dict
        self.left_monkey = left_monkey
        self.right_monkey = right_monkey
        
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
        


for monkey in monkeys:
    
    name = monkey.split(":")[0]

    number = monkey.split(":")[1][1:]

    if any(operation in number for operation in ("+", "*", "-", "/")):

        left_monkey = number.split(" ")[0]
        operation = number.split(" ")[1]
        right_monkey = number.split(" ")[2]
        
        monkeys_dict[name] = MathMonkey(name,monkeys_dict, left_monkey, operation, right_monkey)
        
    else:
        monkeys_dict[name] = YellMonkey(name, int(number))
        
print(monkeys_dict["root"].get_value())