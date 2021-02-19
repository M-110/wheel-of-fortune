"""
Board handles the puzzle and guessed letters
"""
from settings import Settings, Puzzle

test_puzzle = Settings.PUZZLES[0]


class Board:
    """
    Board class
    """

    def __init__(self, puzzle_tuple: Puzzle):
        self._category = puzzle_tuple.category
        self._puzzle_answer = puzzle_tuple.puzzle.upper()
        self._guessed_letters = []
        self._extra_markings = [' ', ',', '"', "'", '-', '.']

    def __repr__(self):
        return f'Board(Puzzle({self.category}, {self.puzzle_answer}))'

    def __str__(self):
        return ''.join([char if char.upper() in (self.guessed_letters + self._extra_markings)
                        else '_' for char in self.puzzle_answer])

    @property
    def category(self):
        """Current category"""
        return self._category

    @property
    def puzzle_answer(self):
        """The full answer"""
        return self._puzzle_answer

    @property
    def guessed_letters(self):
        """Returns copy to keep original list safe"""
        return self._guessed_letters[:]

    def get_masked_puzzle(self):
        """Returns puzzle with letters not yet guessed hidden"""
        return ''.join(char if (char in self.guessed_letters or not char.isalpha()) else '▓'
                       for char in self.puzzle_answer)

    def add_guess(self, letter: str):
        """
        Adds letter to the board's guessed letters
        """
        self._guessed_letters.append(letter.upper())
        print(self)

    def check_if_letter_was_guessed(self, letter: str) -> bool:
        """
        Checks whether a letter has been guessed on this board.

        :param letter: single letter to be checked
        :return: bool: True if letter has been guessed
        """
        return letter.upper() in self.guessed_letters

    def get_letter_count_in_puzzle(self, letter: str) -> int:
        """
        Gets the number of times a letter occurs in the puzzle

        :param letter: single letter to be checked
        :return: int: count of letter in puzzle
        """
        return self.puzzle_answer.count(letter)


empty_board = Board(Puzzle('', ''))
dog = Board(test_puzzle)
