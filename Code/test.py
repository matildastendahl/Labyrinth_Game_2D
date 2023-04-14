"Maze Generation Algorithm Recursive Backtracker"

import sys
import random
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor, QPen, QPainter

class GenerateMaze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
        self.current = self.grid[0][0]

    def generate(self):
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

    def get_unvisited_neighbors(self, cell):
        neighbors = []
        row, col = cell.row, cell.col
        if row > 0 and not self.grid[row - 1][col].visited:  # top
            neighbors.append(self.grid[row - 1][col])
        if col < self.cols - 1 and not self.grid[row][col + 1].visited:  # right
            neighbors.append(self.grid[row][col + 1])
        if row < self.rows - 1 and not self.grid[row + 1][col].visited:  # bottom
            neighbors.append(self.grid[row + 1][col])
        if col > 0 and not self.grid[row][col - 1].visited:  # left
            neighbors.append(self.grid[row][col - 1])
        return neighbors

    def remove_wall(self, cell1, cell2):
        if cell1.row == cell2.row and cell1.col < cell2.col:  # right
            cell1.walls[1] = False
            cell2.walls[3] = False
        elif cell1.row == cell2.row and cell1.col > cell2.col:  # left
            cell1.walls[3] = False
            cell2.walls[1] = False
        elif cell1.col == cell2.col and cell1.row < cell2.row:  # bottom
            cell1.walls[2] = False
            cell2.walls[0] = False
        elif cell1.col == cell2.col and cell1.row > cell2.row:  # top
            cell1.walls[0] = False
            cell2.walls[2] = False

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.walls = [True, True, True, True]  # top, right, bottom, left


class Scene(QGraphicsScene):
    def __init__(self, maze):
        super().__init__()
        self.maze = maze
        self.cell_size = 50
        self.pen = QPen(QColor(0, 0, 0), 5)
        self.brush = QBrush(QColor(0, 0, 0))
        self.draw_maze()

    def draw_maze(self):
        for row in self.maze.grid:
            for cell in row:
                x = cell.col * self.cell_size
                y = cell.row * self.cell_size

                rect_item = QGraphicsRectItem(x, y, self.cell_size, self.cell_size)
                rect_item.setPen(QPen(QColor("white")))
                rect_item.setBrush(QBrush(QColor(255, 255, 255)))
                self.addItem(rect_item)

                if cell.walls[0]:  # top
                    self.addLine(x, y, x + self.cell_size, y, self.pen)
                if cell.walls[1]:  # right
                    self.addLine(x + self.cell_size, y, x + self.cell_size, y + self.cell_size, self.pen)
                if cell.walls[2]:  # bottom
                    self.addLine(x, y + self.cell_size, x + self.cell_size, y + self.cell_size, self.pen)
                if cell.walls[3]:  # left
                    self.addLine(x, y, x, y + self.cell_size, self.pen)

                if cell.visited:
                    rect_item = QGraphicsRectItem(x + 2, y + 2, self.cell_size - 4, self.cell_size - 4)
                    rect_item.setBrush(QBrush(QColor(255, 255, 255)))
                    self.addItem(rect_item)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    maze_generator = GenerateMaze(15, 25)
    maze_generator.generate()

    scene = Scene(maze_generator)
    view = QGraphicsView(scene)
    view.setWindowTitle("Maze")
    view.setRenderHint(QPainter.RenderHint.Antialiasing)
    view.showMaximized()

    sys.exit(app.exec())


