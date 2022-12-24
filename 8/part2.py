import pathlib
import numpy as np
data = pathlib.Path("8/input.txt").read_text()
lines = data.splitlines()
grid_original = [list(map(int,list(line))) for line in lines]
grid_transposed = np.transpose(grid_original).tolist()
counted_scores = np.ones((len(grid_original), len(grid_original[0])))

for index_y, line in enumerate(grid_original):   

    # Check left to right
    for index_x , tree in enumerate(line):
        score_left = 0
        for tree_left in reversed(line[:index_x]):
            score_left += 1
            if tree <= tree_left:
                break
        counted_scores[index_y][index_x] *= score_left
        
        score_right = 0
        for tree_right in line[index_x+1:]:
            score_right += 1
            if tree <= tree_right:
                break
        counted_scores[index_y][index_x] *= score_right

for index_y, line in enumerate(grid_transposed):   
    for index_x , tree in enumerate(line):
        score_left = 0
        for tree_left in reversed(line[:index_x]):
            score_left += 1
            if tree <= tree_left:
                break
        counted_scores[index_x][index_y] *= score_left
        
        score_right = 0
        for tree_right in line[index_x+1:]:
            score_right += 1
            if tree <= tree_right:
                break
        counted_scores[index_x][index_y] *= score_right

print(max(counted_scores.flatten()))
    