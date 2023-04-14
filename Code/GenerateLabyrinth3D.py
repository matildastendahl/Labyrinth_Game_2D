import sys
import random
from PyQt6.QtWidgets import QApplication, QGraphicsView
from PyQt6.QtGui import QPainter
from DrawLabyrinthPyQt import Scene
from Cell import Cell

class GenerateLabyrinth:
#Class to generate labyrinth
    def __init__(self, rows, columns, levels):
        self.rows = rows
        self.columns = columns
        self.levels = levels
        self.grid = [[[Cell(row, column, level) for level in range(levels)] for column in range(columns)] for row in range(rows)]
        self.current = self.grid[0][0][0]
        self.end = self.grid[rows - 1][columns - 1][levels - 1]

    def generate(self):
        #Maze Generation Algorithm: Recursive Backtracker
        stack = []
        while True:
            self.current.visited = True
            neighbors = self.get_unvisited_neighbors(self.current)
            if neighbors:
                neighbor = random.choice(neighbors)
                self.remove_wall(self.current, neighbor)
                stack.append(self.current)
                self.current = neighbor
            elif stack:
                self.current = stack.pop()
            else:
                break

            self.grid[self.rows - 1][self.columns - 1][self.levels - 1].walls[1] = False

    def get_unvisited_neighbors(self, cell):
        neighbors = []
        row = cell.row
        column = cell.column
        level = cell.level

        if row >= 1 and not self.grid[level][row - 1][column].visited:  # up
            neighbors.append(self.grid[level][row - 1][column])

        if row < self.rows - 1 and not self.grid[level][row + 1][column].visited:  # down
            neighbors.append(self.grid[level][row + 1][column])

        if column > 0 and not self.grid[level][row][column - 1].visited:  # left
            neighbors.append(self.grid[level][row][column - 1])

        if column < self.columns - 1 and not self.grid[level][row][column + 1].visited:  # right
            neighbors.append(self.grid[level][row][column + 1])

        if level > 0 and not self.grid[level - 1][row][column].visited:  # above
            neighbors.append(self.grid[level - 1][row][column])

        if level < self.levels - 1 and not self.grid[level + 1][row][column].visited:  # below
            neighbors.append(self.grid[level + 1][row][column])

        return neighbors

    def remove_wall(self, cell1, cell2):
        if cell1.row == cell2.row and cell1.column < cell2.column:  # right
            cell1.walls[1] = False
            cell2.walls[3] = False

        elif cell1.row == cell2.row and cell1.column > cell2.column:  # left
            cell1.walls[3] = False
            cell2.walls[1] = False

        elif cell1.column == cell2.column and cell1.row < cell2.row:  # bottom
            cell1.walls[2] = False
            cell2.walls[0] = False

        elif cell1.column == cell2.column and cell1.row > cell2.row:  # top
            cell1.walls[0] = False
            cell2.walls[2] = False

        elif cell1.level < cell2.level:  # up
            cell1.walls[4] = False
            cell2.walls[5] = False

        elif cell1.level > cell2.level:  # down
            cell1.walls[5] = False
            cell2.walls[4] = False

if __name__ == '__main__':
    app = QApplication(sys.argv)

    labyrinth_generator = GenerateLabyrinth(10, 25, 3)
    labyrinth_generator.generate()

    scene = Scene(labyrinth_generator)
    view = QGraphicsView(scene)
    view.setWindowTitle("Labyrinth")
    view.setRenderHint(QPainter.RenderHint.Antialiasing)
    view.showMaximized()

    sys.exit(app.exec_())