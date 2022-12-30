## Classic bfs

from collections import deque
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
                
def generate_maps(wind_map) -> set:
    global height, width, walls
    for _ in range(math.lcm(width, height)):
        occupied = set().union(walls)
        
        for i in range(len(wind_map)):
            location, direction = wind_map[i]
            location = [((location[0]+direction[0]-1)%width) + 1, ((location[1]+direction[1]-1) % height) + 1]
            wind_map[i][0] = location
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

def find_shortest_path(position, wind_map, limit) -> int:

    directions = [(0,1), (0,-1), (1,0), (-1,0), (0,0)]

    best_score = limit
    found_one = False

    queue = deque()

    queue.append((position, 0))

    visited = dict()

    occupied = list(generate_maps(wind_map))
    
    len_occupied = len(occupied)
    
    max_states = math.lcm(width, height)*(width*height-len(wind_map))
    
    print_interval = 0
    
    
    while queue:

        print_interval += 1

        if print_interval % 1000 == 0:
            print(f"\rQueue Size: {len(queue)} , Explored {len(visited)}/{max_states} possible states, Best Score: {best_score if found_one else -1}{' '*10}", end="")

        position, score = queue.popleft()

        if score + abs(end_x - position[0]) + y_bounds[1] - position[1]  > best_score:
            continue
        
        visited[(position, score%len_occupied)] = score

        if position == (end_x, y_bounds[1]):
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

shortest = -1
SEARCH_LIMIT = 100000
limit = 1
while shortest == -1:
    shortest = find_shortest_path((start_x, y_bounds[0]), wind_map, limit)
    limit *= 2

print()
print(f"Shortest path takes {shortest} minutes")
end_time = datetime.now()
print(f'Calculation took: {(end_time - start_time).seconds}s') 