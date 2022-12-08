import pathlib
data = pathlib.Path("4/input.txt").read_text()
data = data.splitlines()
data = [datum.split(",") for datum in data]
data = [[list(map(int,datum[0].split("-"))),list(map(int,datum[1].split("-")))] for datum in data]

contains = 0

for pair in data:
    binaryReps = []
    for elve in pair:
        binary = 0
        for number in range(elve[0],elve[1]+1):
            binary = 2**(number-1) | binary
        binaryReps.append(binary)
    if binaryReps[0] & binaryReps[1] != 0:
        contains += 1



print(contains)