from math import copysign
import pathlib
data = pathlib.Path("9/input.txt").read_text()
lines = data.splitlines()

instructions = [[line.split(" ")[0], int(line.split(" ")[1])] for line in lines]

visited = [(0,0)]

head = [0,0]
tail = [0,0]

def do_instruction(direction : str , amount : int):
    global head
    if amount == 0:
        return
    match direction:
        case 'U':
            head[0] += 1  
        case 'D':
            head[0] -= 1
        case 'L':
            head[1] -= 1
        case 'R':
            head[1] += 1
    move_tail()
    # print(direction)
    # for y in range(10):
    #     for x in range(10):
    #         if (y,x) == tuple(head):
    #             print("H", end="")
    #         elif (y,x) == tuple(tail):
    #             print("T", end="")
    #         else:
    #             print(".", end="")
    #     print()
    # print()
    do_instruction(direction, amount-1)
    
def move_tail():
    global head
    global tail
    global visited
    
    force_y = head[0] - tail[0]
    force_x = head[1] - tail[1]
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
            
       
   
    tail[0] += force_y_corrected + y_modifier
    tail[1] += force_x_corrected + x_modifier
    
    if tuple(tail) not in visited:
        visited.append(tuple(tail))
        
        
for instruction in instructions:
    do_instruction(instruction[0], instruction[1])
print(len(visited))