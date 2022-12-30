from tqdm import tqdm
import pathlib
lines = pathlib.Path("23/input.txt").read_text().splitlines()


elves = set()

for y in range(len(lines)):
    for x, char in enumerate(lines[y]):
        if char == "#":
            elves.add((x, y))
     
def print_elves(elves):
    x_min, x_max = min(x for x, y in elves), max(x for x, y in elves)
    y_min, y_max = min(y for x, y in elves), max(y for x, y in elves)
    
    for y in range(y_min, y_max+1):
        print(f"{y}:{' '*(3-len(str(y)))}", end="")
        for x in range(x_min, x_max+1):
            if (x, y) in elves:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()
    
directions = ((0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1))

def check_north(elve, neighbors):
    
    if not any((neighbors[0],neighbors[1],neighbors[7])):
        return True, (elve[0],elve[1]-1)

    return False, None

def check_south(elve, neighbors):
    
    if not any((neighbors[3],neighbors[4],neighbors[5])):
        return True, (elve[0],elve[1]+1)

    return False, None

def check_west(elve, neighbors):
    
    if not any((neighbors[5],neighbors[6],neighbors[7])):
        return True, (elve[0]-1,elve[1])

    return False, None

def check_east(elve, neighbors):
    
    if not any((neighbors[1],neighbors[2],neighbors[3])):
        return True, (elve[0]+1,elve[1])

    return False, None

checks = (check_north, check_south, check_west, check_east)

def get_proposition(elves, offset):
    global directions, checks
    offset_og = offset
    propositions = {}
    
    for elve in elves:
        
        neighbors = [(elve[0]+x, elve[1]+y) in elves for x, y in directions]
        proposition = False
        
        offset = offset_og
        
        if any(neighbors):
            for _ in range(4):
                valid, proposition_check = checks[offset](elve, neighbors)
                if valid:
                    proposition = proposition_check
                    break
                offset = (offset+1)%4
            
        if proposition:
            if proposition in propositions:
                propositions[proposition].append(elve)
            else:
                propositions[proposition] = [elve]
                
    return propositions
    


check_offset = 0
rounds = 0

def find_rounds():
    global rounds, check_offset, elves
    while True:
        rounds += 1
        propositions = get_proposition(elves, check_offset)
        check_offset = (check_offset+1)%4
        
        if not propositions:
            yield
            return
        
        for proposition in propositions:
            if len(propositions[proposition]) > 1:
                continue
            elves.remove(propositions[proposition][0])
            elves.add(proposition)
        

        #print_elves(elves)
        yield
        
for _ in tqdm(find_rounds(), desc="Simulated " , unit=" rounds"):
    pass
#print_elves(elves)
print(f"Stopped after {rounds} rounds")
