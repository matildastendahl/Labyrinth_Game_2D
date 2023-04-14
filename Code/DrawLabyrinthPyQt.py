from PyQt6.QtWidgets import QGraphicsScene, QMessageBox, QGraphicsRectItem, QGraphicsEllipseItem, QPushButton, \
    QVBoxLayout, QWidget
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt
from Player import Player


class Scene(QGraphicsScene):
    def __init__(self, labyrinth):
        super().__init__()
        self.labyrinth = labyrinth
        self.player = Player(self.labyrinth.rows, self.labyrinth.columns)
        self.cell_size = 50
        self.pen = QPen(QColor(0, 0, 0), 5)
        self.brush = QBrush(QColor(0, 0, 0))
        self.draw_labyrinth()
        self.draw_player()
        self.update_player_position()

        # Add "help" button
        self.button = QPushButton("Help! Show the way out")
        self.button.clicked.connect(self.show_way_out)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        widget = QWidget()
        widget.setGeometry(-220, 350, 100, 10)
        widget.setLayout(layout)
        self.addWidget(widget)

    def draw_labyrinth(self):
        for row in self.labyrinth.grid:
            for cell in row:
                x = cell.column * self.cell_size
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

    def draw_player(self):
        x = self.player.column * self.cell_size
        y = self.player.row * self.cell_size
        rect_item = QGraphicsRectItem(x, y, self.cell_size, self.cell_size)
        rect_item.setPen(QPen(QColor(0, 0, 0), 5))
        rect_item.setBrush(QBrush(QColor(255, 0, 0)))
        self.addItem(rect_item)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            if not self.labyrinth.grid[self.player.row][self.player.column].walls[0]:
                self.player.row -= 1
        elif event.key() == Qt.Key.Key_Right:
            if not self.labyrinth.grid[self.player.row][self.player.column].walls[1]:
                self.player.column += 1
        elif event.key() == Qt.Key.Key_Down:
            if not self.labyrinth.grid[self.player.row][self.player.column].walls[2]:
                self.player.row += 1
        elif event.key() == Qt.Key.Key_Left:
            if not self.labyrinth.grid[self.player.row][self.player.column].walls[3]:
                self.player.column -= 1
        if self.player.row == self.labyrinth.rows - 1 and self.player.column == self.labyrinth.columns - 1:
            QMessageBox.information(self, "Congratulations", "You solved the game!")

        self.update_player_position()

    def update_player_position(self):
        # Remove old player position
        for item in self.items():
            if isinstance(item, QGraphicsRectItem) and item.brush().color() == QColor(255, 0, 0):
                self.removeItem(item)
                break

        # Add new player position
        x = self.player.column * self.cell_size
        y = self.player.row * self.cell_size
        circle = QGraphicsEllipseItem(x + 5, y + 5, self.cell_size - 10, self.cell_size - 10)
        circle.setPen(QPen(Qt.GlobalColor.red, 2))
        circle.setBrush(QBrush(Qt.GlobalColor.red))
        self.addItem(circle)

    def get_player_position(self):
        return self.player.row, self.player.column

    def show_way_out(self):
        # Find the right way out from the player's current position
        print("Works")
        current_cell = self.labyrinth.grid[self.player.row][self.player.column]
        visited = set()
        path = []

        def dfs(cell):
            print(f"Visiting cell {cell.row}, {cell.column}")
            visited.add(cell)
            if cell == self.labyrinth.grid[-1][-1]:
                return True
            for neighbor in self.labyrinth.get_unvisited_neighbors(cell):
                if neighbor not in visited:
                    if dfs(neighbor):
                        path.append(cell)
                        return True
            print(f"No path found from cell {cell.row}, {cell.column}")
            if path and path[-1] == cell:
                path.remove(cell)
            return False

        dfs(current_cell)
        print(visited)

        # Highlight the path from the player's current position to the exit
        pen = QPen(QColor(0, 255, 0), 5)
        for cell in path:
            x = cell.column * self.cell_size
            y = cell.row * self.cell_size
            rect_item = QGraphicsRectItem(x, y, self.cell_size, self.cell_size)
            rect_item.setPen(pen)
            rect_item.setBrush(QBrush(QColor(0, 0, 0, 0)))
            self.addItem(rect_item)

        print(path)
