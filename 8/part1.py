import pathlib
import numpy as np
data = pathlib.Path("8/input.txt").read_text()
lines = data.splitlines()
grid_original = [list(map(int,list(line))) for line in lines]
grid_transposed = np.transpose(grid_original).tolist()
visible_count = 0
counted = []


for index_y, line in enumerate(grid_original):   
    highest = -1
    # Check left to right
    for index_x , tree in enumerate(line):
        if tree > highest:
            highest = tree
            if (index_x, index_y) not in counted:
                visible_count += 1
                counted.append((index_x, index_y))

    highest = -1
    #check right to left
    for index_x , tree in enumerate(reversed(line)):
        if tree > highest:
            highest = tree
            if (len(line)-index_x-1, index_y) not in counted:
                visible_count += 1
                counted.append((len(line)-index_x-1, index_y))

for index_y, line in enumerate(grid_transposed):   
    highest = -1
    # Check left to right
    for index_x , tree in enumerate(line):
        if tree > highest:
            highest = tree
            if (index_y, index_x) not in counted:
                visible_count += 1
                counted.append((index_y, index_x))

    highest = -1
    #check right to left
    for index_x , tree in enumerate(reversed(line)):
        if tree > highest:
            highest = tree
            if (index_y,len(line)-index_x-1 ) not in counted:
                visible_count += 1
                counted.append((index_y,len(line)-index_x-1))
print(visible_count)
    