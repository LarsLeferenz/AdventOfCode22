import pathlib
lines = pathlib.Path("14/input.txt").read_text().splitlines()

lines = [line.split("->") for line in lines]

# Use set instead of list to speed up the program

occupied = set()

for line in lines:
    for index in range(len(line)-1):
        
        x_start = int(line[index].split(",")[0])
        x_end = int(line[index+1].split(",")[0])

        y_start = int(line[index].split(",")[1])
        y_end = int(line[index+1].split(",")[1])

        if x_start == x_end:
            occupied = occupied.union(((x_start, y) for y in range(min(y_start, y_end),max(y_start, y_end)+1)))
        elif y_start == y_end:
            occupied = occupied.union(((x, y_start) for x in range(min(x_start, x_end),max(x_start, x_end)+1)))
            
floor = max(rock[1] for rock in occupied)

occupied = occupied.union(((x, floor+2) for x in range(200,700)))


def move(sand) -> tuple:
    global occupied, floor
    if (sand[0], sand[1] +1 ) not in occupied:
        sand[1] += 1
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
    occupied = occupied.union((end_location,))
    sand_count += 1
    if sand_count % 100 == 0:
        print(sand_count)
    if end_location == (500,0):
        break
    
print(sand_count)
