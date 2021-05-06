"""
Board handles the puzzle and guessed letters
"""
from typing import List

from settings import Settings, Puzzle

test_puzzle = Settings.PUZZLES[0]


class Board:
    """Board class
    
    Args:
        puzzle: Puzzle to set the board to
    """

    def __init__(self, puzzle: Puzzle):
        self._category = puzzle.category
        self._puzzle_answer = puzzle.puzzle.upper()
        self._guessed_letters = []
        self._extra_markings = [' ', ',', '"', "'", '-', '.']

    def __repr__(self):
        return f'Board(Puzzle({self.category}, {self.puzzle_answer}))'

    def __str__(self):
        return ''.join([char if char.upper() in (self.guessed_letters + self._extra_markings)
                        else '_' for char in self.puzzle_answer])

    @property
    def category(self) -> str:
        """Get current category"""
        return self._category

    @property
    def puzzle_answer(self) -> str:
        """Get the full puzzle answer."""
        return self._puzzle_answer

    @property
    def guessed_letters(self) -> List[str]:
        """Get a copy of a list of guessed letters."""
        return self._guessed_letters[:]
    
    @property
    def masked_puzzle(self):
        """Get the puzzle string but hide letters that are not yet guessed using
        the '▓' character."""
        return ''.join(char if (char in self.guessed_letters or not char.isalpha()) else '▓'
                       for char in self.puzzle_answer)
    
    def add_guess(self, letter: str):
        """Adds letter to the board's guessed letters"""
        self._guessed_letters.append(letter.upper())

    def check_if_letter_was_guessed(self, letter: str) -> bool:
        """
        Checks whether a letter has been guessed on this board. Returns True if
        the letter has already been guessed.

        Args:
            letter: single letter to be checked
        Returns:
             True if letter has been guessed
        """
        return letter.upper() in self.guessed_letters

    def get_letter_count_in_puzzle(self, letter: str) -> int:
        """
        Gets the number of times a letter occurs in the puzzle

        Args:
            letter: single letter to be checked
        Returns:
             count of the letter in puzzle
        """
        return self.puzzle_answer.count(letter)


EMPTY_BOARD = Board(Puzzle('', ''))
