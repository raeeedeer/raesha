class node:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.hcost = 0
        self.depth = 0
        self.c1 = self.c2 = self.c3 = self.c4 = None
        self.expanded = False
