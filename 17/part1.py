import pathlib
from typing import Literal
import itertools
from tqdm import tqdm
intructions = pathlib.Path("17/input.txt").read_text().splitlines()[0]



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
    highest_wall = -6
    
    print("Simulating...")
    for _ in tqdm(range(2022)):
        
        
        to_add = highest_rock - highest_wall + 5
                
        if to_add > 0:
            occupied_spaces = occupied_spaces.union(((0,y) for y in range(highest_wall+1, highest_wall + to_add+1)))
            occupied_spaces = occupied_spaces.union(((8,y) for y in range(highest_wall+1, highest_wall + to_add+1)))
            highest_wall += to_add
            
        rock = Rock(next(rock_iterator), (3, highest_rock+4))
        
        while rock.move(next(instruction_interator), occupied_spaces) and rock.move("down", occupied_spaces):
            pass
    
        #print_board(occupied_spaces, rock)    
        occupied_spaces = occupied_spaces.union(rock.occupied_set())
        highest_rock_test = rock.highest_point()
        if highest_rock_test > highest_rock:
            highest_rock = highest_rock_test
        del rock
        
print(highest_rock)
    