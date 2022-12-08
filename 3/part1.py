def toNumber(s : str) -> int:
    return ord(s) - 96 if s.islower() else ord(s) - 64 + 26

with open('3\input.txt') as f:
    data = f.read()
data = data.splitlines()
data = [list(datum) for datum in data]
data = [list(map(toNumber, datum)) for datum in data]

data = [[sorted(datum[:len(datum)//2], reverse=True), datum[len(datum)//2:]] for datum in data]

score = 0
for rucksack in data:
    for item in rucksack[0]:
        if item in rucksack[1]:
            score += item
            break
print(score)
    


