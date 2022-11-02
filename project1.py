import heapq as min_heap_esque_qu
from msilib.schema import Class
from Node import node
import time
import sys
import copy

goalState = [[1, 2, 3], 
             [4, 5, 6], 
             [7, 8, 0]]
 
def main():
    print("Welcome to Raeed's 8 puzzle solver")
 
    #user Gdecesion for defult puzzle or custom

    trivial = [[1, 2, 3],[4, 5, 6],[7, 8, 0]]
    veryEasy = [[1, 2, 3],[4, 5, 6],[7, 0, 8]]
    easy = [[1, 2, 0],[4, 5, 3],[7, 8, 6]]
    doable = [[0, 1, 2],[4, 5, 3],[7, 8, 6]]
    oh_boy = [[8, 7, 1],[6, 0, 2],[5, 4, 3]]

    Gdecesion = input("type D for default  or C for custom game ")
    Fpuzzle=[]

    if Gdecesion == 'd':
        defaultChoice = input("choosoe a number 1 - 5 with 1 being trivial and 5 being extremely difficult")
        if(defaultChoice == '1'):
            Fpuzzle = trivial
        elif(defaultChoice == '2'):
            Fpuzzle = veryEasy
        elif(defaultChoice == '3'):
            Fpuzzle = easy
        elif(defaultChoice == '4'):
            Fpuzzle = doable
        elif(defaultChoice == '5'):
            Fpuzzle = oh_boy
            
    elif Gdecesion == 'col':
        puzzleValues = input("type each number in your puzzle seperated by a space, 0 is empty space")
        FpuzzleValues = [int(item) for item in puzzleValues.split(' ')]
        r1 = (FpuzzleValues[0],FpuzzleValues[1],FpuzzleValues[2])
        r2 = (FpuzzleValues[3],FpuzzleValues[4],FpuzzleValues[5])
        r3 = (FpuzzleValues[6],FpuzzleValues[7],FpuzzleValues[8])
        Fpuzzle = (r1,r2,r3)

    print("this is your starting puzzle")
    for row in Fpuzzle:
        print(row)
    
    algoDec = input("(1) for uniform cost search. (2) for misplaced tile heuristic. (3) for Manhattan Distacne Heuristic ")
    if algoDec == '1':
        print("executive uniform cost_search")
        #generalSearch(Fpuzzle,0)
    elif algoDec == '2':
        print(" misplaced tile heuristic")
       # generalSearch(Fpuzzle,misplacedTile(Fpuzzle))
    elif algoDec == '3':
        print("Manhattan distance heuristic ")

#generalSearch(Fpuzzle,manhattanDistance(Fpuzzle))
def generalSearch(puzzle, heuristic):
   print("todo")
# Go through the goal puzzle and sum the # of moves needed to return pieces 1-9 to their original spot
def manhattanDistance(puzzle):
    dist = 0
    gr, gc, row, col = 0, 0, 0, 0

    for l in range(8):
        for i in range(len(puzzle)):
            for j in range(len(puzzle)):
                if int(puzzle[i][j]) == l:
                    row = i
                    col = j
                if goalState[i][j] == l:
                    gr = i
                    gc = j
        dist += abs(gr-row) + abs(gc-col)

    return dist

# dist how many tiles are not in the same place (not including the 0 tile)
def misplacedTile(puzzle):
    dist = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if int(puzzle[i][j]) != goalState[i][j] and int(puzzle[i][j]) != 0:
                dist += 1
    return dist

#function used to expand nodes and demonstrate all possible movements for the tile

def repeatstate(loc,noted):
    return(loc not in noted)

def expand(nodeToExp,seen):
    row,col = 0,0
    for i in range(len(nodeToExp.puzzle)):
        for j in range(len(nodeToExp.puzzle)):
            if int(nodeToExp.puzzle[i][j]) == 0:
                row,col = i,j

    if  row > 0: 
        # Resource used for deepcopy: https://docs.python.org/3/library/copy.html
        Sup = copy.deepcopy(nodeToExp.puzzle)
        ph = Sup[row][col]
        Sup[row][col] = Sup[row-1][col]
        Sup[row-1][col] = ph

        if repeatstate(Sup,seen):
            nodeToExp.c3 = node(Sup)

    if  row < len(nodeToExp.puzzle) - 1:
        Sdown = copy.deepcopy(nodeToExp.puzzle)
        ph = Sdown[row][col]
        Sdown[row][col] = Sdown[row + 1][col]
        Sdown[row + 1][col] = ph

        if repeatstate(Sdown,seen):
            nodeToExp.c4 = node(Sdown) 

    if  col > 0:
        Sleft = copy.deepcopy(nodeToExp.puzzle)
        ph = Sleft[row][col]
        Sleft[row][col] = Sleft[row][col - 1]
        Sleft[row][col - 1] = ph
        if repeatstate(Sleft,seen):
            nodeToExp.c1 = node(Sleft)

    if  col < len(nodeToExp.puzzle)-1:
        Sright = copy.deepcopy(nodeToExp.puzzle)
        ph = Sright[row][col]
        Sright[row][col] = Sright[row][col+1]
        Sright[row][col+1] = ph

        if repeatstate(Sright,seen):
            nodeToExp.c2 = node(Sright)

    return nodeToExp

if __name__ == "__main__":
    main()

    