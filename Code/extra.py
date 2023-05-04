def show_way_out(self):
    # Find the right way out from the player's current position
    current_cell = self.labyrinth.grid[self.player.row][self.player.column]
    visited = set()
    path = []

    def dfs(cell):
        visited.add(cell)
        if cell == self.labyrinth.grid[-1][-1]:
            return True
        for neighbor in self.labyrinth.get_unvisited_neighbors(cell):
            if neighbor not in visited:
                if dfs(neighbor):
                    path.append(cell)
                    return True
        if path and path[-1] == cell:
            path.remove(cell)
        return False

    dfs(current_cell)
    print(path)

    # Highlight the path from the player's current position to the exit
    for cell in path:
        x = cell.column * self.cell_size
        y = cell.row * self.cell_size
        circle = QGraphicsEllipseItem(x + 5, y + 5, self.cell_size - 10, self.cell_size - 10)
        circle.setPen(QPen(QColor(255, 0, 0), 2))
        circle.setBrush(QBrush(Qt.transparent))
        self.addItem(circle)