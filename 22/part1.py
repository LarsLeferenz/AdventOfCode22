import pathlib
lines = pathlib.Path("22/input.txt").read_text().splitlines()

def parse_map(lines) -> tuple:
    occupied = set()

    x_bounds = []
    y_bounds = []

    map_stop = 0

    for index_y, line in enumerate(lines):
        
        if line =="":
            map_stop = index_y
            break
                
        x_start = 0
        found_start = False
        for char_index, char in enumerate(line):
            
            if not found_start and char in [".", "#"]:
                x_start = char_index
                found_start = True
            if char == "#":
                occupied.add((char_index, index_y))
                continue
                    
        x_bounds.append((x_start, len(line)-1))

    longest_line = max(len(line) for line in lines[:map_stop])

    for index in range(map_stop+1):
        lines[index] += " "* (longest_line - len(lines[index]))

    for index_x in range(longest_line):
        
        y_start = 0
        found_start = False
        for index_y in range(map_stop+1):
            
            if not found_start and lines[index_y][index_x] in [".", "#"]:
                y_start = index_y
                found_start = True
                continue
            
            if found_start and lines[index_y][index_x] == " ":
                y_bounds.append((y_start, index_y-1))
                break
    
    return occupied, x_bounds, y_bounds, map_stop
            
def parse_instructions(lines, map_stop) -> list:
    import re
    
    number_pattern = re.compile(r"\d+")
    
    instructions = []
    instruction_str = lines[map_stop+1]
    
    for match in re.finditer(number_pattern, instruction_str): 
    
        number = int(match.group())
        instructions.append((number))
        
        if match.end() != len(instruction_str):
            action = instruction_str[match.end()]
            instructions.append((action))
    
    return instructions

def print_field(my_pos, lines, map_stop):
    for y,line in enumerate(lines[:map_stop]):
        for x, char in enumerate(line):
            if (x,y) == my_pos:
                print("X", end="")
                continue
            print(char, end="")
        print()  
    print("\n\n")        

            
occupied, x_bounds, y_bounds, map_stop = parse_map(lines)

instructions = parse_instructions(lines, map_stop)

orientation = ((1,0),(0,1),(-1,0),(0,-1))

orientation_index = 0

my_pos = (x_bounds[0][0], y_bounds[x_bounds[0][0]][0])

for instruction in instructions:
    #print(f"Instruction: {instruction}")
    #print_field(my_pos, lines, map_stop)
    if type(instruction) == str:
        
        if instruction == "L":
            orientation_index = (orientation_index - 1) % 4
        elif instruction == "R":
            orientation_index = (orientation_index + 1) % 4
    else:
        
        heading_x, heading_y = orientation[orientation_index]
        
        for _ in range(instruction):
            
            if orientation_index % 2 == 0:
                new_x = ((my_pos[0] + heading_x - x_bounds[my_pos[1]][0]) % (x_bounds[my_pos[1]][1] - x_bounds[my_pos[1]][0] +1 )) + x_bounds[my_pos[1]][0]
                new_pos = (new_x, my_pos[1])
            
            else:
                new_y = ((my_pos[1] + heading_y - y_bounds[my_pos[0]][0]) % (y_bounds[my_pos[0]][1] - y_bounds[my_pos[0]][0] +1 )) + y_bounds[my_pos[0]][0]
                new_pos = (my_pos[0], new_y)
            
            if new_pos in occupied:
                break
            
            my_pos = new_pos

print(1000*(my_pos[1]+1) + 4*(my_pos[0]+1) + orientation_index)