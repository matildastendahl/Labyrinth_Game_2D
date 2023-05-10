class Player:
# Make player and set start position at middle of grid
    def __init__(self, rows, columns):
        self.row = rows // 2
        self.column = columns // 2
