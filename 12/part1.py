import pathlib
from collections import deque

data = pathlib.Path("12/input.txt").read_text()
lines = data.splitlines()
lines = [list(line) for line in lines]

graph = {f"{y},{x}":[] for x in range(len(lines[0])) for y in range(len(lines))}

start = ""
end = ""

for y, line in enumerate(lines):
    for x, char in enumerate(line):
        value = ord(char)
        
        if char == "S":
            start = f"{y},{x}"
            value = ord("a")
            lines[y][x] = "a"
        elif char == "E":
            end = f"{y},{x}"
            value = ord("z")
            lines[y][x] = "z"
            
        if x != 0:
            if ord(lines[y][x-1])-value <= 1:
                graph[f"{y},{x}"].append(f"{y},{x-1}")
            if ord(lines[y][x-1])-value >= -1:
                graph[f"{y},{x-1}"].append(f"{y},{x}")
        if y != 0:
            if ord(lines[y-1][x])-value <= 1:
                graph[f"{y},{x}"].append(f"{y-1},{x}")
            if ord(lines[y-1][x])-value >= -1:
                graph[f"{y-1},{x}"].append(f"{y},{x}")



# BFS
parent = {start: None}
d = {start: 0}
queue = deque()
queue.append(start)
while queue:
    u = queue.popleft()
    for n in graph[u]:
        if n not in d:
            parent[n] = u
            d[n] = d[u] + 1
            queue.append(n)
            
print(d[end])
