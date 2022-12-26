import pathlib
from datetime import datetime
start = datetime.now()
lines = pathlib.Path("16/input.txt").read_text().splitlines()

graph = {}
flow_rates = {}

for line in lines:
    
    valve = line.split("has")[0][5:].strip()
    
    flow_rate = int(line.split("rate=")[1].split(";")[0])
    
    targets = line.split("lead")[1].split("valve")[1][1:].replace(" ","").split(",")
    
    graph[valve] = targets
    if flow_rate != 0:
        flow_rates[valve] = flow_rate
    
TIME_LIMIT = 30
global_best = 0
pot_score_modifier = 1

def best_pot_left(time_left : int, opened : list) -> int:
    global pot_score_modifier
    score = 0
    remaining = set(flow_rates.keys())-set(opened)
    for valve in remaining:
        score += flow_rates[valve] * (time_left-len(remaining)+ pot_score_modifier)
    return score
    
def explore_neighbors(time : int, location : int, current_score : int, opened : list):
    best_subpath = 0
    time += 1
    for neighbor in graph[location]:
        subpath_score = explore_path(time, neighbor, current_score, opened)
        if subpath_score > best_subpath:
            best_subpath = subpath_score
    return best_subpath

    
def explore_path(time : int, location : int, current_score : int, opened : list	):
    global global_best
    
    if time > TIME_LIMIT:
        return current_score
    
    
    if best_pot_left(TIME_LIMIT-time, opened) + current_score < global_best:
        return current_score
    
    subpath_score_open = 0
    
    if location in flow_rates and location not in opened:
    ## Open valve 
        subpath_score_open = current_score + flow_rates[location] * (TIME_LIMIT-time-1)
        new_opened = opened +[location]
        subpath_score_open = explore_neighbors(time+1, location, subpath_score_open, new_opened)
    
    subpath_score_no_open = explore_neighbors(time, location, current_score, opened)
    
    best_subpath = max(subpath_score_open, subpath_score_no_open)

    if best_subpath >= global_best:
        global_best = best_subpath
        print(f"\rCurrent best:{best_subpath}",end="")
        return best_subpath
    return 0
    
prev_best = 0
id_streak = 0
while True:
    run_best = explore_path(0,"AA",0,[])
    if run_best == prev_best:
        id_streak += 1
    if id_streak == 4:
        break
    prev_best = run_best
    pot_score_modifier *= 1.2
    global_best = run_best
    
end = datetime.now()
print(f"\nSolution: {run_best}; Took: {(end-start).total_seconds()}s")

    