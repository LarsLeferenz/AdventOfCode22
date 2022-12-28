import pathlib
lines = pathlib.Path("18/input.txt").read_text().splitlines()

lines = [tuple(map(int,line.split(","))) for line in lines]

cubes = set(lines)

adjescent = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1))

def get_adjascent_cube_count(cube : tuple):
    global cubes, adjescent

    to_check = ((cube[0] + x, cube[1] + y, cube[2] + z) for x, y, z in adjescent)

    return sum(check in cubes for check in to_check)
    
surface_area = 0

for cube in cubes:
    adjescent_count = get_adjascent_cube_count(cube)
    surface_area += 6 - adjescent_count
    
print(surface_area)
