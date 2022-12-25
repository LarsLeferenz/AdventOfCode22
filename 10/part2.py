import pathlib
data = pathlib.Path("10/input.txt").read_text()
lines = data.splitlines()

lines = [line.split(" ") for line in lines]
instructions = []
for line in lines:
    if len(line) == 2:
        instructions.append([line[0], int(line[1])])
    else:
        instructions.append([line[0]])
        


register_x : int = 1
cycle : int = 0
crt_index : int = 0

def draw_pixel():
    global register_x, crt_index
    if crt_index in {register_x-1, register_x, register_x+1}:
        print("#", end="")
    else:
        print(".", end="")
    crt_index += 1
    if crt_index == 40:
        print()
        crt_index = 0

def inc_cycle():
    global cycle, register_x
    cycle += 1
    draw_pixel()

for instruction in instructions:
    match instruction[0]:
        case "noop":
            inc_cycle()
        case "addx":
            inc_cycle()
            inc_cycle()
            register_x += instruction[1]
            
