from copy import copy
import pathlib
data = pathlib.Path("7/input.txt").read_text()
lines = data.splitlines()

currentDir = {"/":{
    "parent": None,
    "SIZE": 0
}}

topDir = copy(currentDir)

for line in lines:
    if line.startswith("$ cd"):
        if line.startswith("$ cd .."):
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
    
#I'm to lazy to implement something for the last couple of lines :D
currentDir["parent"]["SIZE"] += currentDir["SIZE"]

    
neededSpace =  30000000 - (70000000 - topDir["/"]["SIZE"])

smallestCandidate = 10e10

def exploreSubDirs(dir):
    global smallestCandidate
    if dir["SIZE"] < neededSpace:
        return
    if dir["SIZE"] < smallestCandidate:
        smallestCandidate = dir["SIZE"]
    
    for key, value in dir.items():
        if type(value) == dict and key != "parent":
            exploreSubDirs(value)
            
exploreSubDirs(topDir["/"])
print(smallestCandidate)