# It somehow works in ~40s :D I'm not touching it again

from collections import deque
import pathlib
from datetime import datetime
from tqdm import tqdm
from multiprocessing import Pool
import itertools
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
    
TIME_LIMIT = 26
global_best = 0

def BFS(start) :
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
    return d

distance_maps = { key : BFS(key) for key in graph.keys()}

   

def check_permuations(valves, needed_score = 0):
    global distance_maps, flow_rates
    if len(valves) == 0:
        return 0
    best_score = 0
    for permutation in itertools.permutations(valves):
        my_location = "AA"
        time = 0
        score = 0
        for valve in permutation:
            time += distance_maps[my_location][valve]
            if time < TIME_LIMIT:
                my_location = valve
                time += 1
                score += flow_rates[my_location] * (TIME_LIMIT-time)
            else:
                break
        if score > best_score:
            best_score = score
    return best_score



flow_rate_keys = set(flow_rates.keys())
binary_reps = [2**i for i in range(len(flow_rate_keys))]

iterator_pair = list(zip(binary_reps, flow_rate_keys))

def best_pot_left(time_left : int, potential : list) -> int:
    global flow_rate_keys
    
    return sum(
        flow_rates[valve] * (time_left - len(potential) + 5)
        for valve in potential
    ) 



best_score = 0

def process_asignment(args):
        
        assignment = args[0]
        uneven_factor = args[1]
        
        my_valves = []
        elefants_valves = []
        
        for binary_rep, key in iterator_pair:
            if assignment & binary_rep:
                my_valves.append(key)
            else:
                elefants_valves.append(key)
        
        if len(my_valves) <= len(elefants_valves)//uneven_factor:
            return 0
        if len(elefants_valves) <= len(my_valves)//uneven_factor:
            return 0
        
        my_best_score = check_permuations(my_valves)
        
        
        elefant_best_score = check_permuations(elefants_valves)
        
        return my_best_score + elefant_best_score


def check_distribution(uneven_factor):
    global best_score, iterator_pair, binary_reps
    
    pool = Pool()
    
    assignments = zip(range(binary_reps[-1]), itertools.repeat(uneven_factor))
    
    results = list(tqdm(pool.imap(process_asignment, assignments), total=binary_reps[-1]))
    
    pool.close()
    pool.join()
        
    best_score = max(results)

if __name__ == "__main__":

    print("Brute forcing...")
    check_distribution(1.2)

    end = datetime.now()
    diff = end - start
    print(f"\nBest score: {best_score}; Took {diff.seconds}s")
    