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
cycle_sum : int = 0


def inc_cycle():
    global cycle, register_x, cycle_sum
    cycle += 1
    if cycle in {20, 60, 100, 140, 180, 220}:
        print(f"Cycle {cycle} - Product: {cycle * register_x}")
        cycle_sum += cycle * register_x

for instruction in instructions:
    match instruction[0]:
        case "noop":
            inc_cycle()
        case "addx":
            inc_cycle()
            inc_cycle()
            register_x += instruction[1]
            
print(cycle_sum)
