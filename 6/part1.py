import pathlib
data = pathlib.Path("6/input.txt").read_text()

for index in range(len(data)):
    if len(set(data[index:index+4])) == 4:
        print(index+4)
        break