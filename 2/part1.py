with open('2\input.txt') as f:
    data = f.read()
    data = data.splitlines()

turns = [datum.replace("X","Rock")
         .replace("Y","Paper")
         .replace("Z","Scissors")
         .replace("A","Rock")
         .replace("B","Paper")
         .replace("C","Scissors").split(" ") for datum in data]

score = 0
for turn in turns:
    match turn[1]:
        case "Rock":
            score += 1
            match turn[0]:
                case "Rock": score += 3
                case "Scissors": score += 6
        case "Paper":
            score += 2
            match turn[0]:
                case "Paper": score += 3
                case "Rock": score += 6
        case "Scissors":
            score += 3
            match turn[0]:
                case "Scissors": score += 3
                case "Paper": score += 6        
        
print(score)