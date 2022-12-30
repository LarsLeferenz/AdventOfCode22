## Classic bfs

from collections import deque
from copy import deepcopy
import math
import pathlib
import random
from datetime import datetime
start_time = datetime.now()

lines = pathlib.Path("24/input.txt").read_text().splitlines()

start_x = lines[0].index(".")
end_x = lines[-1].index(".")
x_bounds = (0, len(lines[0])-1)
width = x_bounds[1] - x_bounds[0] -1
y_bounds = (0, len(lines)-1)
height = y_bounds[1] - y_bounds[0] -1
wind_map = []
occupied = set()
walls = set(((start_x,-1),(end_x,y_bounds[1]+1)))
for y,line in enumerate(lines):
    for x,char in enumerate(line):
        match char:
            case "^":
                occupied.add((x,y))
                wind_map.append([[x,y],(0,-1)])
            case ">":
                occupied.add((x,y))
                wind_map.append([[x,y],(1,0)])
            case "v":
                occupied.add((x,y))
                wind_map.append([[x,y],(0,1)])
            case "<":
                occupied.add((x,y))
                wind_map.append([[x,y],(-1,0)])
            case "#":
                walls.add((x,y))
                
def generate_maps(wind_map_global) -> set:
    global height, width, walls
    
    wind_map_local = deepcopy(wind_map_global)
    
    for _ in range(math.lcm(width, height)):
        occupied = set().union(walls)
        
        for i in range(len(wind_map_local)):
            location, direction = wind_map_local[i]
            location = [((location[0]+direction[0]-1)%width) + 1, ((location[1]+direction[1]-1) % height) + 1]
            wind_map_local[i][0] = location
            occupied.add(tuple(location))
            
        yield occupied

def print_winds(occupied):
    global width, height
    for y in range(-1,height+2):
        for x in range(width+2):
            if (x,y) in walls:
                print("#", end="")
            elif (x,y) in occupied:
                print("X", end="")
            else:
                print(".", end="")
        print()
    print()

def find_shortest_path(position, goal, occupied_arg, limit, start_seed) -> int:

    directions = [(0,1), (0,-1), (1,0), (-1,0), (0,0)]

    best_score = limit
    found_one = False

    queue = deque()
    queue.append((position, 0))

    visited = dict()
    occupied = deepcopy(occupied_arg)
    occupied.rotate(-start_seed)
    len_occupied = len(occupied)
    max_states = math.lcm(width, height)*(width*height-len(wind_map))
    
    print_interval = 0
    
    while queue:

        print_interval += 1

        if print_interval % 100 == 0:
            print(f"\rQueue Size: {len(queue)} , Explored {len(visited)}/{max_states} possible states, Best Score: {best_score if found_one else -1}{' '*10}", end="")

        position, score = queue.pop()

        if score > best_score:
            continue
        
        visited[(position, score%len_occupied)] = score

        if position == goal:
            if score < best_score:
                found_one = True
                best_score = score
            continue

        next_occupied = occupied[score%(len(occupied))]

        #random.shuffle(directions)
        for direction in directions:
            new_pos = (position[0] + direction[0], position[1] + direction[1])
            if new_pos not in next_occupied:
                if (new_pos, (score+1)%len_occupied) not in visited or visited[(new_pos, (score+1)%len_occupied)] > score+1:
                    queue.append((new_pos, score+1))

    return best_score if found_one else -1


occupied = deque(generate_maps(wind_map))


shortest_1 = -1
SEARCH_LIMIT = 100000
limit = 50
while shortest_1 == -1 and limit < SEARCH_LIMIT:
    shortest_1 = find_shortest_path((start_x, y_bounds[0]),(end_x, y_bounds[1]), occupied, limit, 0)
    limit *= 2

print()
print(f"Path to goal takes {shortest_1} minutes")

shortest_2 = -1
limit = 50
while shortest_2 == -1 and limit < SEARCH_LIMIT:
    shortest_2 = find_shortest_path((end_x, y_bounds[1]),(start_x, y_bounds[0]), occupied, limit, shortest_1+1)
    limit *= 2
   

print()
print(f"Path back to start takes {shortest_2} minutes")

 
shortest_3 = -1
limit = 50
while shortest_3 == -1 and limit < SEARCH_LIMIT:
    shortest_3 = find_shortest_path((start_x, y_bounds[0]),(end_x, y_bounds[1]), occupied, limit, shortest_1+shortest_2+2)
    limit *= 2


print()
print(f"Path finally to goal takes {shortest_3} minutes")


print()
print(f"Shortest whole path takes {shortest_1+shortest_2+shortest_3+2} minutes")
end_time = datetime.now()
print(f'Calculation took: {(end_time - start_time).seconds}s') 