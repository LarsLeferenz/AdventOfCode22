from collections import deque
from copy import copy
from dataclasses import dataclass
from multiprocessing import Pool
import pathlib
from tqdm import tqdm
from typing import List
lines = pathlib.Path("19/input.txt").read_text().splitlines()


class Blueprint:
    
    def __init__(self, line : str) -> None:
         
        self.ore_robot_cost = int(line.split("ore robot costs ")[1].split("ore")[0])
        self.clay_robot_cost = int(line.split("clay robot costs ")[1].split("ore")[0]) 
        self.obsidian_robot_ore_cost = int(line.split("obsidian robot costs ")[1].split("ore")[0])
        self.obsidian_robot_clay_cost = int(line.split("obsidian robot costs ")[1].split("clay")[0].split("and")[1])
        self.geode_robot_ore_cost = int(line.split("geode robot costs ")[1].split("ore")[0])
        self.geode_robot_obsidian_cost = int(line.split("geode robot costs ")[1].split("obsidian")[0].split("and")[1])

        self.max_ore_cost = max(self.ore_robot_cost, self.clay_robot_cost, self.obsidian_robot_ore_cost, self.geode_robot_ore_cost)


@dataclass
class SimState:
    
    time: int
    
    ore_robots : int
    clay_robots : int
    obsidian_robots : int
    geode_robots : int
    
    ore : int
    clay : int
    obsidian : int
    geodes : int
    
    def __hash__(self):
        return hash((   self.time, 
                        self.ore_robots, 
                        self.clay_robots, 
                        self.obsidian_robots, 
                        self.geode_robots, 
                        self.ore, 
                        self.clay, 
                        self.obsidian, 
                        self.geodes))


blueprints : List[Blueprint]= []

for line in lines[:1]:
    
    blueprints.append(Blueprint(line))
    
    
TIME_LIMIT = 32

def max_score_left(time, sim_state :SimState) -> int:
    time_left = TIME_LIMIT - time
    return sim_state.geode_robots * (time_left) + time_left*(time_left+1)/2
    

def dfs_exploration(blueprint: Blueprint) -> int:
    
    best_score = 0
    
    explored = set()
    
    queue = deque()
    
    init_state = SimState(0, 1, 0, 0, 0, 0, 0, 0, 0)
    
    queue.append(init_state)
    
    while queue:
        
        state : SimState = queue.pop()
        best_score = max(best_score, state.geodes)
        
        if state.time == TIME_LIMIT:
            continue
        
        state.ore = min(state.ore + state.ore_robots, blueprint.max_ore_cost * (TIME_LIMIT-state.time-1))
        state.clay = min(state.clay + state.clay_robots, blueprint.obsidian_robot_clay_cost * (TIME_LIMIT-state.time-1))
        state.obsidian = min(state.obsidian + state.obsidian_robots, blueprint.geode_robot_obsidian_cost * (TIME_LIMIT-state.time-1))
        state.geodes += state.geode_robots
        
        
        
        if hash(state) in explored:
            continue
        
        explored.add(hash(state))
    
        if max_score_left(state.time+1, state) + state.geodes < best_score:
            continue
    
        queue.append(SimState(state.time + 1, 
                              state.ore_robots, 
                              state.clay_robots, 
                              state.obsidian_robots, 
                              state.geode_robots, 
                              state.ore, 
                              state.clay, 
                              state.obsidian, 
                              state.geodes))
    
       
    
    
        if state.ore >= blueprint.ore_robot_cost and state.ore_robots < blueprint.max_ore_cost:
            queue.append(SimState(state.time + 1, 
                                  state.ore_robots + 1, 
                                  state.clay_robots, 
                                  state.obsidian_robots, 
                                  state.geode_robots, 
                                  state.ore - blueprint.ore_robot_cost - 1, 
                                  state.clay, 
                                  state.obsidian, 
                                  state.geodes))
            
        if state.ore >= blueprint.clay_robot_cost and state.clay_robots < blueprint.obsidian_robot_clay_cost:
            queue.append(SimState(state.time + 1, 
                                  state.ore_robots, 
                                  state.clay_robots + 1, 
                                  state.obsidian_robots, 
                                  state.geode_robots, 
                                  state.ore - blueprint.clay_robot_cost, 
                                  state.clay - 1, 
                                  state.obsidian, 
                                  state.geodes))

        if state.ore >= blueprint.obsidian_robot_ore_cost and state.clay >= blueprint.obsidian_robot_clay_cost and state.obsidian_robots < blueprint.geode_robot_obsidian_cost:
            queue.append(SimState(state.time + 1, 
                                  state.ore_robots, 
                                  state.clay_robots, 
                                  state.obsidian_robots + 1, 
                                  state.geode_robots, 
                                  state.ore - blueprint.obsidian_robot_ore_cost, 
                                  state.clay - blueprint.obsidian_robot_clay_cost, 
                                  state.obsidian - 1, 
                                  state.geodes))
    
        if state.ore >= blueprint.geode_robot_ore_cost and state.obsidian >= blueprint.geode_robot_obsidian_cost:
            queue.append(SimState(state.time + 1, 
                                state.ore_robots, 
                                state.clay_robots, 
                                state.obsidian_robots, 
                                state.geode_robots + 1, 
                                state.ore - blueprint.obsidian_robot_ore_cost,
                                state.clay, 
                                state.obsidian - blueprint.geode_robot_obsidian_cost, 
                                state.geodes-1))

            
        
        
    return best_score
def test_blueprint(args):
    blueprint = args[0]
    bp_id = args[1] 
    bp1_score = dfs_exploration(blueprint)
    print(bp1_score)
    return bp1_score
    

if __name__ == "__main__":
    
    tasks = zip(blueprints, range(1,len(blueprints)+1))
    results = []
    
    for task in tasks:
        results.append(test_blueprint(task))
    
    #pool = Pool(3)
    
    #results = list(tqdm(pool.imap(test_blueprint, tasks), total=len(blueprints)))
    
    #pool.close()
    #pool.join()
    
    print(results)