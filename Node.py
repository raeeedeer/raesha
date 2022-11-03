class node:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.hc = 0
        self.depth = 0
        self.child1 = self.child2 = self.child3 = self.child4 = None
        self.expanded = False
   
   #node class with all relevent parameters for each puzzle state