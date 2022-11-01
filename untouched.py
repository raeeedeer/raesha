import time
import sys
from Node import node
import copy







# Go through the goal puzzle and sum the # of moves needed to return pieces 1-9 to their original spot





def manhattanDistance(puzzle):
    goal_pzl = [[2, 2, 3], [4, 5, 6], [7, 8, 0]]
    count = 0
    gr, gc, r, c = 0, 0, 0, 0

    for l in range(1, 9):
        for i in range(len(puzzle)):
            for j in range(len(puzzle)):
                if int(puzzle[i][j]) == l:
                    r = i
                    c = j
                if goal_pzl[i][j] == l:
                    gr = i
                    gc = j
        count += abs(gr-r) + abs(gc-c)

    return count


# Count how many tiles are not in the same place (not including the 0 tile)
def misplacedTile(puzzle):
    count = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if int(puzzle[i][j]) != goalState[i][j] and int(puzzle[i][j]) != 0:
                count += 1
    return count

#function used to expand nodes and demonstrate all possible movements for the tile

def repeatstate(loc,noted):
    return(loc not in noted)

def expand(NTE,seen):
    r,c = 0,0
    for i in range(len(NTE.puzzle)):
        for j in range(len(node.puzzle)):
            if int(NTE.puzzle[i][j]):
                r,c = i,j

    if  r > 0: 
        up = copy.deepcopy(NTE.puzzle)
        temp = up[r][c]
        up[r][c] = up[r-1][c]
        up[r-1][c] = temp

        if repeatstate(up,seen):
            NTE.c1 = node(left)

    if  r < len(NTE.puzzle) - 1:
        # Resource used for deepcopy: https://docs.python.org/3/library/copy.html
        down = copy.deepcopy(NTE.puzzle)
        temp = down[r][c]
        down[r][c] = down[r + 1][c]
        down[r + 1][c] = temp

    if  c > 0:
    # Resource used for deepcopy: https://docs.python.org/3/library/copy.html
        left = copy.deepcopy(nd.puzzle)
        temp = left[r][c]
        left[r][c] = left[r][c - 1]
        left[r][c - 1] = temp
    
    if  c < len(nd.puzzle)-1:
    # Resource used for deepcopy: https://docs.python.org/3/library/copy.html
        right = copy.deepcopy(nd.puzzle)
        temp = right[r][c]
        right[r][c] = right[r][c+1]
        right[r][c+1] = temp
                