"""Test the Puzzle class"""
from wheel_of_fortune.puzzle import Puzzle


def test_content():
    puzzle = Puzzle()
    assert puzzle.content == "Hello"