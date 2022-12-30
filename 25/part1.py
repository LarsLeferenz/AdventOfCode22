import pathlib
import math
lines = pathlib.Path("25/input.txt").read_text().splitlines()


def translate_snafu(char):
    match char:
        case "=":
            return -2
        case "-":
            return -1
        case _:
            return int(char)
        
        
total = 0
for line in lines:
    number = 0
    for digit,char in enumerate(reversed(line)):
        number += 5**digit * translate_snafu(char)
    total += number
    
    

    
snafu_number = ""
digit = 1
while total != 0:
    
    
    remainder = total%5**digit
    total -= remainder
    
    
    if remainder > 2*(5**(digit-1)):
        total += 5**digit
        char = "-" if remainder == 4*(5**(digit-1)) else "="
    else:
        char = str(remainder//(5**(digit-1)))
        
    snafu_number = char + snafu_number
     
    digit += 1
     
    
print(snafu_number)
    
    
    