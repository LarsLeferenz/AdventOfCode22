# Solution for abitray number of nodes

from math import copysign
import pathlib
data = pathlib.Path("9/input.txt").read_text()
lines = data.splitlines()

instructions = [[line.split(" ")[0], int(line.split(" ")[1])] for line in lines]

visited = []

NODE_COUNT = 10

rope = [[0,0] for _ in range(NODE_COUNT)]

def move_head(direction : str , amount : int):
    global rope
    if amount == 0:
        return
    match direction:
        case 'U':
            rope[0][0] += 1  
        case 'D':
            rope[0][0] -= 1
        case 'L':
            rope[0][1] -= 1
        case 'R':
            rope[0][1] += 1
    for node in range(1, len(rope)):
        follow_node(node-1, node)
    if tuple(rope[-1]) not in visited:
        visited.append(tuple(rope[-1]))
        
    move_head(direction, amount-1) # Unnassary recursion ftw :D
    
def follow_node(node: int, follower :int):
    global rope
    force_y = rope[node][0] - rope[follower][0]
    force_x = rope[node][1] - rope[follower][1]
    force_y_corrected = force_y
    force_x_corrected = force_x
    x_modifier = 0
    y_modifier = 0
    
    if abs(force_x) <= 1 and abs(force_y) <= 1:
        return
    
    if force_x != 0:
        force_x_corrected -= copysign(1,force_x)
        
    if force_y != 0:
        force_y_corrected -= copysign(1,force_y)
   
    if force_x != 0 and force_y != 0:
        y_modifier = abs(force_x_corrected) * copysign(1,force_y) 
        x_modifier = abs(force_y_corrected) * copysign(1,force_x)
    
    # Could be combined with clever maths, but I can't be bothered
    
    if abs(force_y_corrected + y_modifier)!= 0:  
        rope[follower][0] += copysign(1,force_y_corrected + y_modifier)
    if abs(force_x_corrected + x_modifier)!= 0:
        rope[follower][1] += copysign(1,force_x_corrected + x_modifier)
    
def print_rope():
    global rope
    print("Rope:")
    for y in range(10,-10,-1):
        for x in range(-13,13):
            if [y,x] in rope:
                print(rope.index([y,x]), end="")
            else:
                print(".", end="")
        print()   
        
for instruction in instructions:
    move_head(instruction[0], instruction[1])
    #print_rope()
print(len(visited))
# for y in range(15,-15,-1):
#     for x in range(-15,15):
#         if (y,x) in visited:
#             print("#", end="")
#         else:
#             print(".", end="")
#     print()
    
    
