import pathlib
data = pathlib.Path("13/input.txt").read_text()
lines = data.splitlines()


lines = [eval(line) for line in lines if line != ""]


def int_compare(left, right) -> str:
    if left == right:
        return "continue"
    else:
        return "right_order" if left < right else "wrong_order"
    
def compare(left, right, state) -> str:
    if state in {"wrong_order", "right_order"}:
        return state
    
    if type(left) == list and type(right) == int:
        right = [right]
    
    if type(left) == int and type(right) == list:
        left = [left]
    
    if type(left) == list and type(right) == list:
        to_check = zip(left, right)
        new_state = "continue"
        for left_check, right_check in to_check:
            new_state = compare(left_check, right_check, "continue")
            if new_state != "continue":
                return new_state
        if len(left) > len(right):
            return "wrong_order"
        elif len(right) > len(left):
            return "right_order"
        else:
            return "continue"
        
    if type(left) == int and type(right) == int:
        return int_compare(left, right)
    
    
lines.append([[2]])
lines.append([[6]])
    
packets_sorted = [lines[0]]

# bubble sort

for packet in lines[1:]:
    inserted = False
    for index, packet_sorted in enumerate(packets_sorted):
        state = compare(packet, packet_sorted, "continue")
        if state == "right_order":
            packets_sorted.insert(index, packet)
            inserted = True
            break
        if state == "wrong_order":
            continue
    if not inserted:
        packets_sorted.append(packet)
    
# for packet in packets_sorted:
#     print(packet)

start_index = packets_sorted.index([[2]]) +1
end_index = packets_sorted.index([[6]]) +1

print(start_index*end_index)