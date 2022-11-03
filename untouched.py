import copy
import time
import sys


def main():
    print('Welcome to Danial\'s 8 puzzle solver!')

    # Getting user input for if they want to use default or their own
    inputsel = input('Please type “1” to use a default puzzle, or “2” to enter your own puzzle!'
                     ' Please be sure to press ENTER after making your choice!\n')
    inputnum = int(inputsel)

    # Setting up puzzle if user uses a custom puzzle
    if inputnum == 1:
        puzzle = (['1', '2', '3'], ['4', '0', '6'], ['7', '5', '8'])
    elif inputnum == 2:
        print('Enter your puzzle, use a zero to represent the blank \n')

        # Getting the first row
        row1 = input('Enter the first row, use spaces between numbers: ')

        # Getting the seconodeToExp row
        row2 = input('Enter the seconodeToExp row, use spaces between numbers: ')

        # Getting the third row
        row3 = input('Enter the third row, use spaces between numbers: ')

        print('\n')

        # Combining input into a puzzle
        row1 = row1.split(' ')
        row2 = row2.split(' ')
        row3 = row3.split(' ')

        puzzle = row1, row2, row3

    # Allowing the user to choose heuristic
    algo = input('Enter your choice of algorithm \n1. Uniform Cost Search '
                 '\n2. A* with the Misplaced Tile heuristic. \n3. A* with the Manhattan distance heuristic\n')
    qf = int(algo)

    # Running the program anodeToExp printing the output
    print(generalsearch(puzzle, qf))

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


# Main "driver" program inspired by the psuedocode in the assignment PDF
def generalsearch(problem, queuefunc):

    # Getting the time when general search starts and setting a 15 minute (900s) duration
    starttime = time.time()
    duration = 900

    # Variable definition
    #     'q' is our queue, seen is all the puzzles we've seen already, ncount is nodes visited,
    #      qsz tracks the size of the queue and mq tracks the max size of the queue at any time
    q = []
    seen = []
    ncount = -1
    qsz = 0
    mq = -1

    # Calculating heuristic based on the user inputted heuristic
    if queuefunc == 1:
        h = 0
    if queuefunc == 2:
        h = misplaced(problem)
    if queuefunc == 3:
        h = manhattan(problem)

    # Creating the start node, with the puzzle, depth of 0, and heuristic. We then add the node to the queue
    # and list it in the seen array.
    n = node(problem)
    n.hcost = h
    n.depth = 0
    q.append(n)

    seen.append(n.puzzle)
    qsz +=1
    mq += 1

    # Loop until we finish solving a problem
    while True:
        # Sort the queue for the lowest h(n) + g(n)
        if queuefunc != 1 and h >= 0:
            # Utilizing a lambda function instead to make sorting faster - sorts by lowest h(n) + g(n)
            # and by depth if there's a tie
            # Resource for sorting: https://docs.python.org/3/howto/sorting.html
            q = sorted(q, key=lambda x: (x.depth + x.hcost, x.depth))

        # If the queue is empty we can't do anything
        if len(q) == 0:
            return 'Failure :('

        # Remove the first node, increase node visited count but decrease queue size
        nd = q.pop(0)
        if nd.expanded == False:
            ncount += 1
            nd.expanded = True
        qsz -= 1

        # If we make it to goal state print some data
        if goal(nd.puzzle):
            return ('Goal!! \n\nTo solve this problem the search algorithm expanded a total of ' +
                  str(ncount) + ' nodes.\nThe maximum number of nodes in the queue at any one time was '
                  + str(mq) + '.\nThe depth of the goal node was ' + str(nd.depth) + '\n\nCPU Time: ' +
                    str(time.time()-starttime) + ' seconds')

        # Skipping on the first occasion to allow it to first decide which node is best to expand
        if ncount != 0:
            print('The best state to expand with a g(n) = ' + str(nd.depth) + ' and h(n) = ' + str(nd.hcost)
                  + ' is...\n' + str(nd.puzzle) + '\tExpanding this node...\n')
        else:
            print('\nExpanding state: ' + str(nd.puzzle) + '\n')

        # Expand all possible states from the node popped off the queue and put them into child nodes
        exnd = expand(nd, seen)

        # Loop through the array of children and modify stats based on the expanded puzzles based on heuristics chosen
        # by the user. The depth is the depth of the parent node (node popped off queue + 1).
        arr = [exnd.c1, exnd.c2, exnd.c3, exnd.c4]

        for i in arr:
            if i is not None:
                if queuefunc == 1:
                    i.depth = nd.depth + 1
                    i.hcost = 0
                elif queuefunc == 2:
                    i.depth = nd.depth + 1
                    i.hcost = misplaced(i.puzzle)
                elif queuefunc == 3:
                    i.depth = nd.depth + 1
                    i.hcost = manhattan(i.puzzle)

                # Add these states to the queue and add them to a list of states we have now seen
                q.append(i)
                seen.append(i.puzzle)
                qsz += 1

        # Change the max queue size if it has been surpassed
        if qsz > mq:
            mq = qsz

        # If we go over the 15 minutes, have the program exit with a message saying it ran out of time
        # Resource used to track the time + duration of program: https://www.programiz.com/python-programming/time
        if time.time() > starttime + duration:
            print('Ran out of time')
            sys.exit()



# Go through the goal puzzle anodeToExp sum the # of moves needed to return pieces 1-9 to their original spot
def manhattan(puzzle):
    goal_pzl = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
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
def misplaced(puzzle):
    goal_pzl = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    count = 0

    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if int(puzzle[i][j]) != goal_pzl[i][j] and int(puzzle[i][j]) != 0:
                count += 1
    return count


# Check if the input puzzle matches the goal puzzle
def goal(puzzle):
    goal_pzl = (['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0'])

    if puzzle == goal_pzl:
        return True
    return False


# Node definition, stores puzzle, depth, heuristic cost, 4 children, anodeToExp an expanodeToExped boolean
# 4 children because we can have at most 4 sub-scenarios from a particular state of where 0 can be moved
class node:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.hcost = 0
        self.depth = 0
        self.c1 = self.c2 = self.c3 = self.c4 = None
        self.expanded = False


if __name__ == "__main__":
    main()
