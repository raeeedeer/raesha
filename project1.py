import heapq as min_heap_esque_qu
from msilib.schema import Class
import queue
from Node import node
import time
import sys
 #used for deepcopy: https://docs.python.org/3/library/copy.html
import copy


goalState = [[1, 2, 3], 
             [4, 5, 6], 
             [7, 8, 0]]
 
def main():
    print("Welcome to Raeed's 8 puzzle solver")

    puzzle = puzzleConfig()
 
    #user decesion for defult puzzle or custom
    algoDec = input("(1) for uniform cost search. (2) for misplaced tile heuristic. (3) for Manhattan Distacne Heuristic ")
    print(generalSearch(puzzle,int(algoDec)))
#function to configure puzzle 
def puzzleConfig():
    depth0 = [[1,2,3],[4,5,6],[7,8,0]]
    depth2 = [[1,2,3],[4,5,6],[0,7,8]]
    depth4 = [[1,2,3],[5,0,6],[4,7,8]]
    depth8 = [[1,3,6],[5,0,2],[4,7,8]]
    depth12 = [[1,3,6],[5,0,7],[4,8,2]]
    depth16 = [[1,6,7],[5,0,3],[4,8,2]]
    depth20 = [[7,1,2],[4,8,5],[6,3,0]]

    Gdecesion = input("type D for default  or C for custom game ")
    startingPuzzle=[]

    if Gdecesion == 'd':
        defaultChoice = input("choose a number 1 - 7 with 1 being trivial and 7 being extremely difficult")
        if(defaultChoice == '1'):
            startingPuzzle = depth0
        elif(defaultChoice == '2'):
            startingPuzzle = depth2
        elif(defaultChoice == '3'):
            startingPuzzle = depth4
        elif(defaultChoice == '4'):
            startingPuzzle = depth8
        elif(defaultChoice == '5'):
            startingPuzzle = depth12
        elif(defaultChoice == '6'):
            startingPuzzle = depth16
        elif(defaultChoice == '7'):
            startingPuzzle = depth20
    #allows custom input
    elif Gdecesion == 'c':
        puzzleValues = input("type each number in your puzzle seperated by a space, 0 is empty space")
        FpuzzleValues = [int(item) for item in puzzleValues.split(' ')]
        r1 = [FpuzzleValues[0],FpuzzleValues[1],FpuzzleValues[2]]
        r2 = [FpuzzleValues[3],FpuzzleValues[4],FpuzzleValues[5]]
        r3 = [FpuzzleValues[6],FpuzzleValues[7],FpuzzleValues[8]]
        startingPuzzle = [r1,r2,r3]

    print("this is your starting puzzle")
    for row in startingPuzzle:
        print(row)

    return startingPuzzle


#main driver of program 
def generalSearch(puzzle, heuristic):

    #starting time of general search
    st = time.time()
    #duration of 2k seconds 
    duration = 2000
    #determine heuristic based on h value
    if heuristic == 1:
        h = uniformCostSearch(puzzle)
    if heuristic == 2:
        h = misplacedTile(puzzle)
    elif heuristic == 3:
        h = manhattanDistance(puzzle)

    #nq = main queue
    nq = []  
    #starting node
    treeNode = node(puzzle)
    treeNode.hc, treeNode.depth = h,0
    nq.append(treeNode)

    #tracks all seen states
    statesTracker = []
    nodeCounter = -1
    #queue size and max queue size
    qsize = 0
    qmax = -1

    statesTracker.append(treeNode.puzzle)
    qsize+=1


    while True:
        qmax = max(qmax,len(nq))
        if heuristic != 0 and h>=0:
            #using lmbda function to make sorting faster
            nq = sorted(nq, key=lambda x: (x.depth + x.hc, x.depth))
        #if empty return failure 
        if len(nq) == 0:
            return "Failure"
        #if not expanded, expand
        currNode = nq.pop(0)
        if currNode.expanded == False:
            nodeCounter += 1
            currNode.expanded = True

        qsize -= 1
        #if goal state is found print depth, time taken, nodes expanded, and max queue size
        if currNode.puzzle == goalState:
            return ('Goal state! \n solution depth ' +
                  str(currNode.depth) +'\n number of nodes expanded: '
                  + str(nodeCounter) + '.\n Max queue size: ' + str(qmax) + '\n\nCPU Time: ' +
                    str(time.time()-st) + ' seconds')
        
        if nodeCounter != 0:
            print('The best state to expand with a g(n) = ' + str(currNode.depth) + ' and h(n) = ' + str(currNode.hc)
                  + ' is...\n' + str(currNode.puzzle) + '\tExpanding this node...\n')
        else:
            print('\nExpanding state: ' + str(currNode.puzzle) + '\n')
        #expands children of parent node
        expNode = expand(currNode,statesTracker)
        nodeChildren = [expNode.child1, expNode.child2, expNode.child3, expNode.child4]
        #loop through children and modify based on heuristic
        for child in nodeChildren:
            if child is not None:
                if heuristic == 1:
                    child.depth = currNode.depth+1
                    child.hc = 0
                elif heuristic == 2:
                    child.depth = currNode.depth +1
                    child.hc = misplacedTile(child.puzzle)
                elif heuristic == 3:
                    child.depth = currNode.depth + 1
                    child.hc = manhattanDistance(child.puzzle)
                
                nq.append(child)
                statesTracker.append(child.puzzle)
                qsize +=1
        
       



def uniformCostSearch(puzzle):
    return 0
#sum number of moves needed for all misplaced tiles to retun to goal state
def manhattanDistance(puzzle):
    dist = 0
    gr, gc, row, col = 0, 0, 0, 0

    for l in range(1,9):
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
#calcuate how many tiles are misplaced
def misplacedTile(puzzle):
    dist = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if int(puzzle[i][j]) != goalState[i][j] and int(puzzle[i][j]) != 0:
                dist += 1
    return dist

#determine if state is a repeatstate to ignore
def repeatstate(loc,noted):
    return(loc not in noted)
#shows all possible ways to move space within puzzle
def expand(nodeToExp,seen):
    row,col = 0,0
    for i in range(len(nodeToExp.puzzle)):
        for j in range(len(nodeToExp.puzzle)):
            if int(nodeToExp.puzzle[i][j]) == 0:
                row,col = i,j

    if  row > 0: 
        Sup = copy.deepcopy(nodeToExp.puzzle)
        ph = Sup[row][col]
        Sup[row][col] = Sup[row-1][col]
        Sup[row-1][col] = ph

        if repeatstate(Sup,seen):
            nodeToExp.child3 = node(Sup)

    if  row < len(nodeToExp.puzzle) - 1:
        Sdown = copy.deepcopy(nodeToExp.puzzle)
        ph = Sdown[row][col]
        Sdown[row][col] = Sdown[row + 1][col]
        Sdown[row + 1][col] = ph

        if repeatstate(Sdown,seen):
            nodeToExp.child4 = node(Sdown) 

    if  col > 0:
        Sleft = copy.deepcopy(nodeToExp.puzzle)
        ph = Sleft[row][col]
        Sleft[row][col] = Sleft[row][col - 1]
        Sleft[row][col - 1] = ph
        if repeatstate(Sleft,seen):
            nodeToExp.child1 = node(Sleft)

    if  col < len(nodeToExp.puzzle)-1:
        Sright = copy.deepcopy(nodeToExp.puzzle)
        ph = Sright[row][col]
        Sright[row][col] = Sright[row][col+1]
        Sright[row][col+1] = ph

        if repeatstate(Sright,seen):
            nodeToExp.child2 = node(Sright)

    return nodeToExp

if __name__ == "__main__":
    main()

