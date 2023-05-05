from PyQt6.QtWidgets import QGraphicsScene, QMessageBox, QGraphicsLineItem, QGraphicsRectItem, QGraphicsEllipseItem, QPushButton, \
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
        self.start = self.labyrinth.grid[self.labyrinth.rows//2][self.labyrinth.columns//2]
        self.end = self.labyrinth.grid[-1][-1]
        self.visited = set()
        self.path = []
        self.path_items = []

        # Add "help" button
        self.button = QPushButton("Help! Show the way out")
        self.button.clicked.connect(self.buttonclicked)

        # Add "New Game" button
        self.new_game_button = QPushButton("New Game")
        self.new_game_button.clicked.connect(self.start_new_game)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.new_game_button)
        self.widget = QWidget()
        self.widget.setGeometry(-220, 350, 100, 10)
        self.widget.setLayout(layout)
        self.addWidget(self.widget)

    def buttonclicked(self):
        if self.button.text() == "Help! Show the way out":
            self.button.setText("Hide solution")
            self.show_way_out()
        else:
            self.button.setText("Help! Show the way out")
            self.hide_solution()

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
        rect_item = QGraphicsEllipseItem(x, y, self.cell_size, self.cell_size)
        rect_item.setPen(QPen(QColor(0, 0, 0), 5))
        rect_item.setBrush(QBrush(QColor(255, 0, 0)))
        self.addItem(rect_item)

    def start_new_game(self):
        # Restart the game
        self.clear()
        self.labyrinth.generate()
        self.player = Player(self.labyrinth.rows, self.labyrinth.columns)
        self.draw_labyrinth()
        self.draw_player()
        self.update_player_position()
        self.start = self.labyrinth.grid[self.labyrinth.rows//2][self.labyrinth.columns//2]
        self.end = self.labyrinth.grid[-1][-1]
        self.visited = set()
        self.path = []
        self.path_items = []


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
            reply = QMessageBox.question(self.parent(), "Congratulations", "You won the game! Do you want to play again?",
                                         QMessageBox.StandardButton.Yes)
            if reply == QMessageBox.StandardButton.Yes:
                self.start_new_game()
        self.update_player_position()

    def update_player_position(self):
        # Remove old player position
        for item in self.items():
            if isinstance(item, QGraphicsEllipseItem) and item.brush().color() == QColor(Qt.GlobalColor.red):
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

    def hide_solution(self):
        for line in self.path_items:
            self.removeItem(line)
        self.path_items.clear()
        self.path.clear()


    def show_way_out(self):
        for row in self.labyrinth.grid:
            for cell in row:
                cell.visited = False
        if self.dfs(self.start):
            # Highlight the path from the player's current position to the exit
            for i in range(len(self.path) - 1):
                start_cell = self.path[i]
                end_cell = self.path[i + 1]
                x1 = start_cell.column * self.cell_size + self.cell_size / 2
                y1 = start_cell.row * self.cell_size + self.cell_size / 2
                x2 = end_cell.column * self.cell_size + self.cell_size / 2
                y2 = end_cell.row * self.cell_size + self.cell_size / 2
                line = QGraphicsLineItem(x1, y1, x2, y2)
                line.setPen(QPen(QColor(255, 0, 0), 2))
                self.addItem(line)
                self.path_items.append(line)

            return list(reversed(self.path))


    def dfs(self, cell):
        print(f"Current cell: {cell}")
        neighbors = self.labyrinth.get_neighbors(cell)
        print(f"Unvisited neighbors: {neighbors}")
        if cell == self.end:
            # we have found the end cell, so return True
            self.path.append(cell)
            return True

        # mark the current cell as visited
        self.visited.add(cell)
        print(f"Visited: {self.visited}")

        # loop through the adjacent cells
        for neighbor in self.labyrinth.get_neighbors(cell):
            print(cell, self.end, self.visited, self.path)
            if neighbor not in self.visited:
                self.path.append(neighbor)
                if self.dfs(neighbor):
                    print(f"Found path to end: {self.path}")
                    return True
                self.path.pop()
                print(f"Path: {self.path}")
        return False


