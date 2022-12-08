import pathlib
data = pathlib.Path("5/input.txt").read_text()
data = data.splitlines()

cargo_data = data[:8]
instructions = data[10:]


stacks = [[] for _ in range(9)];

for line in reversed(cargo_data):
    seperated_line = []
    for index in range(0,35,4):
        item = line[index:index+4]
        item = item.replace("[","").replace("]","").replace(" ","")
        seperated_line.append(item)
    for index, item in enumerate(seperated_line):
        if item != "":
            stacks[index].append(item)

for instruction in instructions:
    instruction = instruction.split(" ")
    amount = int(instruction[1])
    origin_stack = int(instruction[3])-1
    target_stack = int(instruction[5])-1
    for _ in range(amount):
        stacks[target_stack].append(stacks[origin_stack].pop())

tops = [stack[-1] for stack in stacks]
print("".join(tops))