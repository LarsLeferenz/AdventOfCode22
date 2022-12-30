
## Sadly doesn't work, I guess something in the edge teleports is wrong, but debugging this is pain :D

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

def print_field_with_history(history, lines, map_stop):
    
    headings = (">", "v", "<", "^")
    
    file = open("22/history.txt", "w")
    
    for y,line in enumerate(lines[:map_stop]):
        for x, char in enumerate(line):
            pos = (x,y)
            found_history = False
            for pos_history, orientation in reversed(history):
                if  pos == pos_history:
                    print(headings[orientation], end="")
                    file.write(headings[orientation])
                    found_history = True
                    break
            if found_history:
                continue
            print(char, end="")
            file.write(char)
        print()  
        file.write("\n")
    print("\n\n")       
    file.close() 


def add_translation(source : dict, origin_tuple : tuple, origin_range : range , target_tuple : tuple, target_range : range, target_direction : tuple):

    assert len(origin_range) == len(target_range)

    dimension_origin = origin_tuple.index("x")

    if dimension_origin == 0:
        origin = ((i, origin_tuple[1]) for i in origin_range)
    else :
        origin = ((origin_tuple[0], i) for i in origin_range)

    dimension_target = target_tuple.index("x")

    if dimension_target == 0:
        target = (((i, target_tuple[1]),target_direction) for i in target_range)
    else:
        target = (((target_tuple[0], i), target_direction) for i in target_range)

    translation = {str(a): b for a, b in zip(origin, target)}

    return source | translation


def get_cube_teleports():
    
    teleports =  {}
    
    x = "x"
    
    #### EDGE 1 #######
    
    teleports = add_translation(teleports, 
                                (x, -1), range(50, 100),
                                (0, x), range(150, 200), (1,0))
    
    teleports = add_translation(teleports, 
                                (-1,x ), range(150, 200),
                                (x, 0), range(50, 100), (0,1))
    
    #### EDGE 2 #######
    
    teleports = add_translation(teleports, 
                                (x, -1), range(100, 150),
                                (x, 199), range(0, 50), (0,-1))
    
    teleports = add_translation(teleports, 
                                (x,200), range(0, 50),
                                (x, 0), range(100, 150),(0,1))
 
    #### EDGE 3 #######
    
    teleports = add_translation(teleports, 
                                (x, 150), range(50, 100),
                                (49, x), range(150, 200), (-1,0))
    
    teleports = add_translation(teleports, 
                                (50, x), range(150, 200),
                                (x, 149), range(50, 100), (0,-1))
    
    
    #### EDGE 4 #######
    
    teleports = add_translation(teleports, 
                                (x, 50), range(100, 150),
                                (99, x), range(50, 100), (-1,0))
    
    teleports = add_translation(teleports, 
                                (100, x), range(50, 100),
                                (x, 49), range(100, 150), (0,-1))
 
    #### EDGE 5 #######
    
    teleports = add_translation(teleports, 
                                (150, x), range(0, 50),
                                (49, x), range(149, 99,-1), (-1,0))
    
    teleports = add_translation(teleports, 
                                (100, x), range(149, 99, -1),
                                (149, x), range(0, 50), (-1,0))
    
    #### EDGE 6 #######
    
    teleports = add_translation(teleports, 
                                (49, x), range(50, 100),
                                (x, 100), range(49, -1, -1), (0,-1))
    
    teleports = add_translation(teleports, 
                                (x, 99), range(49, -1, -1),
                                (50, x), range(50, 100), (1,0))   
    
    #### EDGE 7 #######
    
    teleports = add_translation(teleports, 
                                (49, x), range(0, 50),
                                (0, x), range(149, 99, -1), (1,0)) 
    
    teleports = add_translation(teleports, 
                                (-1, x), range(149, 99, -1),
                                (50, x), range(0, 50), (1,0))
    
    
    return teleports
    

            
occupied, x_bounds, y_bounds, map_stop = parse_map(lines)

instructions = parse_instructions(lines, map_stop)

teleports = get_cube_teleports()

orientations = ((1,0),(0,1),(-1,0),(0,-1))

orientation_index = 0

my_pos = (x_bounds[0][0], y_bounds[x_bounds[0][0]][0])

pos_history = [[(0,0),0]]

for instruction in instructions:

    
    #print(f"Instruction: {instruction}")
    #print_field(my_pos, lines, map_stop)
    if type(instruction) == str:
        
        if instruction == "L":
            orientation_index = (orientation_index - 1) % 4
        elif instruction == "R":
            orientation_index = (orientation_index + 1) % 4
            
        pos_history[-1][1] = orientation_index
    else:
        
        for _ in range(instruction):
            
            heading_x, heading_y = orientations[orientation_index]
            
            
            new_pos = (my_pos[0] + heading_x, my_pos[1] + heading_y)
            new_orientation_index = orientation_index
            
            if str(new_pos) in teleports:
                new_pos, heading = teleports[str(new_pos)]
                new_orientation_index = orientations.index(heading)
            
            if new_pos in occupied:
                break
            
            assert new_pos[0] >= 0 and new_pos[1] >= 0, f"new_pos: {new_pos}"
            
            
            pos_history.append([new_pos, new_orientation_index])
            orientation_index = new_orientation_index
            my_pos = new_pos

#print_field_with_history(pos_history, lines, map_stop)
print(1000*(my_pos[1]+1) + 4*(my_pos[0]+1) + orientation_index)