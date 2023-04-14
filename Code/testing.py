from GenerateLabyrinth import GenerateLabyrinth
from DrawLabyrinthPyQt import Scene
import unittest
from unittest import TestCase


class Test(TestCase):
    def test_rows_and_columns(self):
        # Test rows: 15, columns: 25
        labyrinth = GenerateLabyrinth(15, 25)
        labyrinth.generate()
        assert len(labyrinth.grid) == 15
        assert len(labyrinth.grid[0]) == 25

        # Test rows: 5, columns 5
        labyrinth = GenerateLabyrinth(5, 5)
        labyrinth.generate()
        assert len(labyrinth.grid) == 5
        assert len(labyrinth.grid[0]) == 5

        # Test rows: 20, columns 7
        labyrinth = GenerateLabyrinth(20, 7)
        labyrinth.generate()
        assert len(labyrinth.grid) == 20
        assert len(labyrinth.grid[0]) == 7

if __name__ == '__main__':
    unittest.main()

