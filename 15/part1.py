import pathlib
lines = pathlib.Path("15/input.txt").read_text().splitlines()

lines = [line.split(":") for line in lines]

pairs = []

for line in lines:
    sensor_x = int(line[0].split(",")[0].split("=")[1])
    sensor_y = int(line[0].split(",")[1].split("=")[1])

    beacon_x = int(line[1].split(",")[0].split("=")[1])
    beacon_y = int(line[1].split(",")[1].split("=")[1])

    distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

    pairs.append(((sensor_x, sensor_y), (beacon_x, beacon_y), distance))



Y_LINE = 2000000

# remove definitifly to far away ones

pruned_pairs = [pair for pair in pairs if abs(pair[0][1] - Y_LINE) <= pair[2]]

beacons_on_line = set(pair[1] for pair in pruned_pairs if pair[1][1] == Y_LINE)

covered_x = set()
for pair in pruned_pairs:
    
    distance_to_y = abs(pair[0][1] - Y_LINE)
    remaining_distance = pair[2] - distance_to_y
    
    covered_x = covered_x.union(range(pair[0][0] - remaining_distance, pair[0][0] + remaining_distance + 1))


print(len(covered_x)-len(beacons_on_line))