import pathlib
from typing import Literal
import itertools
from tqdm import tqdm
intructions = pathlib.Path("17/input.txt").read_text().splitlines()[0]

data_file = open("17/data.txt", "w")

class Rock():
    
    def __init__(self, shape : Literal["-","+","J","I","#"], position : tuple) -> None:
        
        self.occupied_spaces = ()
        self.position = position
        match shape:
            case "-": 
                self.occupied_spaces = ((0,0),(1,0),(2,0),(3,0))
            case "+":
                self.occupied_spaces = ((0,1),(1,0),(1,1),(1,2),(2,1))
            case "J":
                self.occupied_spaces = ((0,0),(1,0),(2,0),(2,1),(2,2))
            case "I":
                self.occupied_spaces = ((0,0),(0,1),(0,2),(0,3))
            case "#":
                self.occupied_spaces = ((0,0),(1,0),(0,1),(1,1))
                
    def move(self, direction : Literal[">","<","down"], occupied : set) -> bool:
        match direction:
            case ">":
                new_position = (self.position[0] + 1, self.position[1])
                if self.check_colision(occupied, new_position):
                    return True
                else:
                    self.position = new_position
            case "<":
                new_position = (self.position[0] - 1, self.position[1])
                if self.check_colision(occupied, new_position):
                    return True
                else:
                    self.position = new_position
            case "down":
                new_position = (self.position[0], self.position[1]-1)
                if self.check_colision(occupied, new_position):
                    return False
                else:
                    self.position = new_position
        return True
    def check_colision(self, occupied : set, new_position : tuple):
        
        my_spaces = ((x +new_position[0], y + new_position[1]) for x,y in self.occupied_spaces)
        return any(my_space in occupied for my_space in my_spaces)
                
    def occupied_set(self) -> set:
        
        return set((x +self.position[0], y + self.position[1]) for x,y in self.occupied_spaces)
        
    def highest_point(self) -> int:
        
        return max(self.occupied_spaces, key = lambda x: x[1])[1]+self.position[1]
                
def print_board(occupied_spaces : set, rock : Rock):

    rock_occupies = rock.occupied_set()
    highest_rendered = max(occupied_spaces, key = lambda x: x[1])[1] + 1
    
    for index_y in range(highest_rendered, 0,-1):
        for index_x in range(0, 9):
            if index_x == 0 or index_x == 8:
                print("|", end="")
            elif (index_x, index_y) in occupied_spaces:
                print("#", end="")
            elif (index_x, index_y) in rock_occupies:
                print("@", end="")
            else:
                print(".", end="")
        print()
    print("".join(["-" for _ in range(9)]))
        



if __name__ == "__main__":
    
    rock_iterator = itertools.cycle(["-","+","J","I","#"])
    instruction_interator = itertools.cycle(intructions)
    occupied_spaces = set(((x,0) for x in range(9)))
    
    highest_rock = 0
    prev_highest_entry = 0
    highest_wall = -6
    floor = 0
    print("Simulating...")
    for rock_count in tqdm(range(5000)):
        
        
        to_add = highest_rock - highest_wall + 5
                
        if to_add > 0:
            occupied_spaces = occupied_spaces.union(((0,y) for y in range(highest_wall+1, highest_wall + to_add+1)))
            occupied_spaces = occupied_spaces.union(((8,y) for y in range(highest_wall+1, highest_wall + to_add+1)))
            highest_wall += to_add
            
        rock = Rock(next(rock_iterator), (3, highest_rock+4))
        
        while True:
            rock.move(next(instruction_interator), occupied_spaces) 
            if not rock.move("down", occupied_spaces):
                break
            pass
    
        
    
        #print_board(occupied_spaces, rock)    
        occupied_spaces = occupied_spaces.union(rock.occupied_set())
        highest_rock_test = rock.highest_point()
        
        prev_highest_entry = highest_rock
        
        if highest_rock_test > highest_rock:
            highest_rock = highest_rock_test
        del rock
        
        if highest_rock > floor + 100 :
            for y in range(floor, floor + 50):
                for x in range(0,9):
                    if (x,y) in occupied_spaces:
                        occupied_spaces.remove((x,y))
            floor += 50
            
        
        data_file.write(f"{highest_rock-prev_highest_entry},")
        
    data_file.close()

    print("Extrapolating cycle...")

    import re
    
    def repetitions(s):
        r = re.compile(r"(.+?)\1+")
        for match in r.finditer(s):
            yield (match.group(1), len(match.group(0))/len(match.group(1)))



    data = pathlib.Path("17/data.txt").read_text()

    increase_repetion = list(repetitions(data))

    cylce_str = max(increase_repetion, key = lambda x: len(x[0]))[0][1:]

    cylce_start = data.find(cylce_str)

    sum_before_cycle = sum(int(x) for x in data[:cylce_start].split(",")[:-1])

    cylce_sum = sum(int(x) for x in cylce_str.split(","))

    cycles_needed = (1000000000000 - len(data[:cylce_start].split(",")[:-1])) // len(cylce_str.split(","))

    rock_remaining = (1000000000000 - len(data[:cylce_start].split(",")[:-1])) % len(cylce_str.split(","))

    total_sum = sum_before_cycle + (cylce_sum * cycles_needed) + sum(int(x) for x in cylce_str.split(",")[:rock_remaining])

    print(total_sum)
        