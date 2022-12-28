from copy import deepcopy
import sys

sys.setrecursionlimit(10000)

import pathlib
import numpy as np
lines = pathlib.Path("18/input.txt").read_text().splitlines()

lines = [tuple(map(int,line.split(","))) for line in lines]

cubes = set(lines)
cubes_np = np.transpose(list(cubes))

x_bounds = (min(cubes_np[0]) -1, max(cubes_np[0])+1)
y_bounds = (min(cubes_np[1]) -1, max(cubes_np[1])+1)
z_bounds = (min(cubes_np[2]) -1, max(cubes_np[2])+1)


adjescent = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1))

def get_open_faces(cube : tuple):
    global cubes, adjescent

    to_check = ((cube[0] + x, cube[1] + y, cube[2] + z) for x, y, z in adjescent)

    return {check for check in to_check if check not in cubes}
    
water = set()


def fill_water_adjecent(coord : tuple, depth : 0):
    global water, x_bounds, y_bounds, z_bounds
    if depth > 500:
        return
    for side in adjescent:
        
        target = (coord[0] + side[0], coord[1] + side[1], coord[2] + side[2])
        
        if target in water :
            continue
        
        if target in cubes:
            continue
        
        if target[0] < x_bounds[0] or target[0] > x_bounds[1]:
            continue
        
        if target[1] < y_bounds[0] or target[1] > y_bounds[1]:
            continue
        
        if target[2] < z_bounds[0] or target[2] > z_bounds[1]:
            continue
        
        water.add(target)
        
        fill_water_adjecent(target, depth + 1)
        

def fill_water_general():
    global water, x_bounds, y_bounds, z_bounds
    for x in range(x_bounds[0]-1, x_bounds[1] + 2):
        for y in range(y_bounds[0]-1, y_bounds[1] + 2):
            for z in range(z_bounds[0]-1, z_bounds[1] + 2):
                if (x,y,z) in cubes:
                    break
                water.add((x,y,z))
            for z in range(z_bounds[1]+1, z_bounds[0]-1, -1):
                if (x,y,z) in cubes:
                    break
                water.add((x,y,z))   
   
surface_area = 0
fill_water_general()

for water_drop in deepcopy(water): 

    fill_water_adjecent(water_drop,0)

for cube in cubes:
    open_faces = get_open_faces(cube)
    
    surface_faces = {face for face in open_faces if face in water}
        
    surface_area += len(surface_faces)
    
print(surface_area)
