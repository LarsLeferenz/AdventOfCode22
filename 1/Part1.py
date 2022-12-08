import pathlib
data = pathlib.Path("1/input.txt").read_text()
dataSep = data.split("\n\n")
elves = [elve.split("\n") for elve in dataSep]
print(max(sum(list(map(int, elve))) for elve in elves))
    