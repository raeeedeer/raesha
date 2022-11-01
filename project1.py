import heapq as min_heap_esque_qu
from msilib.schema import Class

goalState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

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
        defaultChoice = input("choose a number 1 - 5 with 1 being trivial and 5 being extremely difficult")
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
            
    elif Gdecesion == 'c':
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
    starting_node = TreeNode.TreeNode(None, puzzle, 0, 0)
    working_queue = []
    repeated_states = dict()
    min_heap_esque_queue.heappush(working_queue, starting_node)
    num_nodes_expanded = 0
    max_queue_size = 0
    repeated_states[starting_node.board_to_tuple()] = "This is the parent board"

    stack_to_print = [] # the board states are stored in a stack

    while len(working_queue) > 0:
        max_queue_size = max(len(working_queue), max_queue_size)
        # the node from the queue being considered/checked
        node_from_queue = min_heap_esque_queue.heappop(working_queue)
        repeated_states[node_from_queue.board_to_tuple()] = "This can be anything"
        if node_from_queue.solved(): # check if the current state of the board is the solution
            while len(stack_to_print) > 0: # the stack of nodes for the traceback
                print_puzzle(stack_to_print.pop())
            print("Number of nodes expanded:", num_nodes_expanded)
            print("Max queue size:", max_queue_size)
            return node_from_queue

        stack_to_print.append(node_from_queue.board)



if __name__ == "__main__":
    main()