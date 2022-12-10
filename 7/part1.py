from copy import copy
import pathlib
data = pathlib.Path("7/input.txt").read_text()
lines = data.splitlines()

currentDir = {"/":{
    "parent": None,
    "SIZE": 0
}}

sizeUnder = 0

for line in lines:
    if line.startswith("$ cd"):
        if line.startswith("$ cd .."):
            if currentDir["SIZE"] < 100000:
                sizeUnder += currentDir["SIZE"]
            currentDir["parent"]["SIZE"] += currentDir["SIZE"]
            currentDir = currentDir["parent"]
            continue
        targetDir = line.split(" ")[2]
        currentDir = currentDir[targetDir]
        continue
    if line.startswith("$ ls"):
        continue
    if line.startswith("dir"):
        newDir = line.split(" ")[1]
        currentDir[newDir] = {  "parent": currentDir,
                                "SIZE": 0}
        continue
    file = line.split(" ")[1]
    size = int(line.split(" ")[0])
    currentDir[file] = size
    currentDir["SIZE"] += size
    
print(sizeUnder)