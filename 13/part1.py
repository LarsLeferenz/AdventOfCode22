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
    
index_sum = 0    
     
for index in range(0,len(lines),2):
    state =compare(lines[index], lines[index+1], "continue")    
    if state == "right_order":
        index_sum += int(index/2 + 1)
    
print(index_sum)