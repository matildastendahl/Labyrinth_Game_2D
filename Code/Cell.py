class Cell:
# Generating a cell, which the labyrinth is concluded of
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.visited = False
        self.walls = [True, True, True, True]  # top, right, bottom, left
