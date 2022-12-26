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

pairs = sorted(pairs, key=lambda x: x[0][0])

def is_overlaping(a, b):
    return b[0] > a[0] and b[0] < a[1]

def merge_intervals(arr):
    arr.sort(key = lambda x: x[0])

    merged_list= []
    merged_list.append(arr[0])
    for i in range(1, len(arr)):
        pop_element = merged_list.pop()
        if is_overlaping(pop_element, arr[i]):
            new_element = pop_element[0], max(pop_element[1], arr[i][1])
            merged_list.append(new_element)
        else:
            merged_list.append(pop_element)
            merged_list.append(arr[i])
    return merged_list


for current_y in range(4000000):
    covered_x = []
    for pair in pairs:
        distance_to_y = abs(pair[0][1] - current_y)
        remaining_distance = pair[2] - distance_to_y
        if remaining_distance >=0:   
            covered_x.append((max(0,pair[0][0] - remaining_distance), min(4000000,pair[0][0] + remaining_distance) ))

    covered_x = merge_intervals(covered_x)

    if len(covered_x) != 1:
        for index in range(1,len(covered_x)):
            if covered_x[index-1][1]+1 < covered_x[index][0]:
                print(f"\nFOUND IT: {current_y + 4000000 * (covered_x[index-1][1]+1)}")
                exit()
                
    if current_y % 10000 == 0:
        print(f"\rLeft to check: {4000000-current_y}" , end="")




input()
    
    
    

