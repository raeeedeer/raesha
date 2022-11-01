class node:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.hcost = 0
        self.depth = 0
        self.c1 = None
        self.c2 = None
        self.c3 = None
        self.c4 = None
        self.expanded = False
