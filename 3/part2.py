def toNumber(s : str) -> int:
    return ord(s) - 96 if s.islower() else ord(s) - 64 + 26

with open('3\input.txt') as f:
    data = f.read()
data = data.splitlines()
data = [list(datum) for datum in data]
rucksacks = [list(map(toNumber, datum)) for datum in data]

score = 0
for index in range(0, len(data), 3):
    for item in rucksacks[index]:
        if item in rucksacks[index+1] and item in rucksacks[index+2]:
            score += item
            break
            
print(score)
    


