from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QApplication, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QPen, QColor
from PyQt6.QtCore import Qt
import sys
import random

labyrinth_height = 22
labyrinth_width = 22
direction = [(1, 0), (0, 1), (-1, 0), (0, -1)]


class Labyrinth(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Labyrinth")
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, parent = self)
        self.setCentralWidget(self.view)

        self.cell_size = 20
        self.grid = [[0 for x in range(labyrinth_width)] for y in range(labyrinth_height)]

    def labyrinth_generator(self):
        "Prim's Algorithm"
        x = 2
        y = 2

        for i in range(labyrinth_width):
            self.grid[0][i] = 1
            self.grid[labyrinth_height - 1][i] = 1
        for i in range(labyrinth_height):
            self.grid[i][0] = 1
            self.grid[i][labyrinth_width - 1] = 1

        while True:
            self.grid[y][x] = 1
            random.shuffle(direction)
            random_direction = list(direction)
            for k, l in random_direction:
                if self.grid[y + l][x + k] == 0:
                    self.grid[y + l // 2][x + k // 2] = 1
                    x = x + k
                    y = y + l
                    break
            else:
                break
        return self.grid

    def draw_labyrinth(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                rect = QGraphicsRectItem(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if cell == 0:
                    rect.setBrush(QColor("white"))
                elif cell == 1:
                    rect.setBrush(QColor("black"))
                self.scene.addItem(rect)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    labyrinth = Labyrinth()
    labyrinth.labyrinth_generator()
    labyrinth.draw_labyrinth()
    labyrinth.show()
    sys.exit(app.exec())

