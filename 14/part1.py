# Pretty slow

import pathlib
lines = pathlib.Path("14/input.txt").read_text().splitlines()

lines = [line.split("->") for line in lines]

occupied = []

for line in lines:
    for index in range(len(line)-1):
        
        x_start = int(line[index].split(",")[0])
        x_end = int(line[index+1].split(",")[0])

        y_start = int(line[index].split(",")[1])
        y_end = int(line[index+1].split(",")[1])

        if x_start == x_end:
            occupied.extend((x_start, y) for y in range(min(y_start, y_end),max(y_start, y_end)+1))
        elif y_start == y_end:
            occupied.extend((x, y_start) for x in range(min(x_start, x_end),max(x_start, x_end)+1))
            
floor = max(rock[1] for rock in occupied)

def move(sand) -> tuple:
    global occupied, floor
    if (sand[0], sand[1] +1 ) not in occupied:
        sand[1] += 1
        if sand[1] > floor:
            return (-1,-1)
        return move(sand)
    elif (sand[0] -1, sand[1]+1) not in occupied:
        sand[0] -= 1
        sand[1] += 1
        return move(sand)
    elif (sand[0] +1, sand[1]+1) not in occupied:
        sand[0] += 1
        sand[1] += 1
        return move(sand)
    
    return tuple(sand)



sand_count = 0
            
while True:
    
    sand = [500,0]
    end_location = move(sand)
    if end_location == (-1,-1):
        break
    occupied.append(end_location)
    sand_count += 1
    
print(sand_count)
