import pathlib
data = pathlib.Path("6/input.txt").read_text()

for index in range(len(data)):
    if len(set(data[index:index+14])) == 14:
        print(index+14)
        break