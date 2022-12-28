from dataclasses import dataclass
from multiprocessing import Pool
import pathlib
from tqdm import tqdm
from typing import List
from datetime import datetime
start = datetime.now()
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
    
    time: int = 0
    
    ore_robots : int = 1
    clay_robots : int = 0
    obsidian_robots : int = 0
    geode_robots : int = 0
    
    ore : int = 0
    clay : int = 0
    obsidian : int = 0
    geodes : int = 0
    
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

for line in lines[:3]:
    
    blueprints.append(Blueprint(line))
    
    

    
    
TIME_LIMIT = 32

def max_score_left(time, sim_state :SimState) -> int:
    time_left = TIME_LIMIT - time
    return sim_state.geode_robots * (time_left) + time_left*(time_left+1)/2
   
global_best = 0

explored = set()

def simulate_step(state: SimState, blueprint: Blueprint ) -> int:
    global global_best

    if state.time == TIME_LIMIT:
        return state.geodes
    
    state.ore = min(state.ore + state.ore_robots, blueprint.max_ore_cost * (TIME_LIMIT-state.time-1))
    state.clay = min(state.clay + state.clay_robots, blueprint.obsidian_robot_clay_cost * (TIME_LIMIT-state.time-1))
    state.obsidian = min(state.obsidian + state.obsidian_robots, blueprint.geode_robot_obsidian_cost * (TIME_LIMIT-state.time-1))
    state.geodes += state.geode_robots
    
    
    internal_state = hash(state)
    
    if internal_state in explored:
        return 0
    
    explored.add(internal_state)
    
    
    best_subpath = 0
    
    if max_score_left(state.time, state) + state.geodes < global_best:
        return 0
    
    
    best_nothing, best_ore, best_clay, best_obsidian, best_geode = 0, 0, 0, 0, 0
    

    if state.ore >= blueprint.geode_robot_ore_cost and state.obsidian >= blueprint.geode_robot_obsidian_cost:
        best_geode = simulate_step(SimState(state.time + 1, 
                            state.ore_robots, 
                            state.clay_robots, 
                            state.obsidian_robots, 
                            state.geode_robots + 1, 
                            state.ore - blueprint.obsidian_robot_ore_cost,
                            state.clay, 
                            state.obsidian - blueprint.geode_robot_obsidian_cost, 
                            state.geodes-1), blueprint)
    


    if state.ore >= blueprint.ore_robot_cost and state.ore_robots < blueprint.max_ore_cost:
        best_ore = simulate_step(SimState(state.time + 1, 
                                state.ore_robots + 1, 
                                state.clay_robots, 
                                state.obsidian_robots, 
                                state.geode_robots, 
                                state.ore - blueprint.ore_robot_cost - 1, 
                                state.clay, 
                                state.obsidian, 
                                state.geodes), blueprint)
        
    if state.ore >= blueprint.clay_robot_cost and state.clay_robots < blueprint.obsidian_robot_clay_cost:
       best_clay = simulate_step(SimState(state.time + 1, 
                                state.ore_robots, 
                                state.clay_robots + 1, 
                                state.obsidian_robots, 
                                state.geode_robots, 
                                state.ore - blueprint.clay_robot_cost, 
                                state.clay - 1, 
                                state.obsidian, 
                                state.geodes), blueprint)

    if state.ore >= blueprint.obsidian_robot_ore_cost and state.clay >= blueprint.obsidian_robot_clay_cost and state.obsidian_robots < blueprint.geode_robot_obsidian_cost:
        best_obsidian = simulate_step(SimState(state.time + 1, 
                                state.ore_robots, 
                                state.clay_robots, 
                                state.obsidian_robots + 1, 
                                state.geode_robots, 
                                state.ore - blueprint.obsidian_robot_ore_cost, 
                                state.clay - blueprint.obsidian_robot_clay_cost, 
                                state.obsidian - 1, 
                                state.geodes), blueprint)



    best_nothing = simulate_step(SimState(state.time + 1, 
                                    state.ore_robots, 
                                    state.clay_robots, 
                                    state.obsidian_robots, 
                                    state.geode_robots, 
                                    state.ore, 
                                    state.clay, 
                                    state.obsidian, 
                                    state.geodes), blueprint)

    best_subpath = max(best_nothing, best_ore, best_clay, best_obsidian, best_geode)
    if best_subpath > global_best:
        global_best = best_subpath
    
    return best_subpath
    
    



def test_blueprint(args):
    global global_best, explored
    blueprint = args[0]
    bp_id = args[1] 
    global_best = 0
    explored = set()
    bp1_score = simulate_step(SimState(), blueprint)
    return bp1_score 
    

if __name__ == "__main__":
    
    tasks = zip(blueprints, range(1,len(blueprints)+1))
    
    pool = Pool()
    
    results = list(tqdm(pool.imap(test_blueprint, tasks), total=len(blueprints)))
    
    pool.close()
    pool.join()
    
    print(results)
    print(f"Product: {results[0]*results[1]*results[2]}")
    end = datetime.now()
    diff = end - start
    print(f"Took {diff.seconds}s")
    