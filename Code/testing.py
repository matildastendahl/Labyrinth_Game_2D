import unittest
from unittest import TestCase
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from Player import Player
from GenerateLabyrinth import GenerateLabyrinth
from DrawLabyrinthPyQt import Scene


class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the QApplication before running the tests
        cls.app = QApplication([])

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

    def test_button_clicked(self):
        labyrinth = GenerateLabyrinth(15, 25)
        labyrinth.generate()
        scene = Scene(labyrinth)
        self.assertEqual(scene.button.text(), "Help! Show the way out")
        QTest.mouseClick(scene.button, Qt.MouseButton.LeftButton)
        self.assertEqual(scene.button.text(), "Hide solution")
        QTest.mouseClick(scene.button, Qt.MouseButton.LeftButton)
        self.assertEqual(scene.button.text(), "Help! Show the way out")

    @classmethod
    def tearDownClass(cls):
        # Clean up and quit the QApplication after running the tests
        cls.app.quit()

if __name__ == '__main__':
    unittest.main()

