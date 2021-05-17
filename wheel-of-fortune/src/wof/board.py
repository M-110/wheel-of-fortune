"""
Board handles the puzzle and guessed letters
"""
from string import ascii_uppercase
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
        """Get or set the full puzzle answer."""
        return self._puzzle_answer

    @puzzle_answer.setter
    def puzzle_answer(self, answer):
        self._puzzle_answer = answer

    @property
    def guessed_letters(self) -> List[str]:
        """Get a copy of a list of guessed letters."""
        return self._guessed_letters[:]

    @property
    def vowels_remain(self) -> bool:
        """True if there are still non-guessed vowels in the puzzle."""
        return len([char for char in self.puzzle_answer
                    if (char not in self.guessed_letters and
                        char in "AEIOU")]) > 0

    @property
    def letters_remain(self) -> bool:
        """True if there are any non-guessed letters in the puzzle."""
        return len([char for char in self.puzzle_answer
                    if char not in self.guessed_letters and
                    char in ascii_uppercase]) > 0

    @property
    def solved_percent(self) -> float:
        """Get the percent of the puzzle that is solved"""
        total_letters = len([char for char in self.puzzle_answer
                             if char in ascii_uppercase])
        total_solved_letters = len([char for char in self.puzzle_answer
                                    if char in self.guessed_letters])
        print(self.puzzle_answer)
        return total_solved_letters / total_letters

    @property
    def masked_puzzle(self):
        """Get the puzzle string but hide letters that are not yet guessed using
        the '▓' character."""
        return ''.join(char if (char in self.guessed_letters or not char.isalpha()) else '▓'
                       for char in self.puzzle_answer)
    
    def reveal(self):
        """Reveals the puzzle fully by adding all letters to guessed letters."""
        self._guessed_letters = list(ascii_uppercase)

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
    
    def check_if_puzzle_guess_is_right(self, guess: str):
        """Returns True if puzzle guess was correct."""
        return reduce_phrase(self.puzzle_answer) == reduce_phrase(guess)
        

def reduce_phrase(phrase: str) -> str:
    """Reduce a phrase down to just alphabetical characters and space."""
    return ''.join([char for char in phrase
                    if (char.isalpha() or char == ' ')])


EMPTY_BOARD = Board(Puzzle('', ''))
