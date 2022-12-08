with open('2\input.txt') as f:
    data = f.read()
    data = data.splitlines()

turns = [datum.replace("A","Rock")
         .replace("B","Paper")
         .replace("C","Scissors")
         .replace("X","Lose")
         .replace("Y","Draw")
         .replace("Z","Win").split(" ") for datum in data]

score = 0
for turn in turns:
    match turn[0]:
        case "Rock":
            match turn[1]:
                case "Lose": score += 0 + 3
                case "Draw": score += 3 + 1
                case "Win": score += 6 + 2
        case "Paper":
            match turn[1]:
                case "Lose": score += 0 + 1
                case "Draw": score += 3 + 2
                case "Win": score += 6 + 3
        case "Scissors":
            match turn[1]:
                case "Lose": score += 0 + 2
                case "Draw": score += 3 + 3
                case "Win": score += 6 + 1
                
print(score)