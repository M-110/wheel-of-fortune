﻿from typing import List, Tuple, Callable
from settings import Settings
from settings import Prize
from settings import Character
import random

from src.wof.board import Board
from src.wof.parsers import spin_solve_vowel_parser_factory, CONSONANT_GUESS_PARSERS, VOWEL_GUESS_PARSERS, \
    SOLUTION_GUESS_PARSERS

ALPHABET = Settings.ALPHABET
VOWELS = Settings.VOWELS
MOST_COMMON_LETTERS = Settings.MOST_COMMON_LETTERS


class Player:
    """
    Base class for players.
    
    Args:
        name: name of the player
        bio: a short bio of the player.
    """

    def __init__(self, game_state, name: str = '', bio: str = ''):
        self._name = name
        self._bio = bio
        self._game_state = game_state
        self._total_cash = 0
        self._round_cash = 0
        self._total_prizes = []
        self._round_prizes = []

    def __repr__(self):
        return f'<{self.__class__.name} name={self.name}>'

    def __str__(self):
        return f'{self.name}:\n\ttotal cash: {self.total_cash}\n\tround_cash: {self.round_cash}'

    @property
    def name(self) -> str:
        """Get the player's name."""
        return self._name

    @property
    def bio(self) -> str:
        """Get the player's bio."""
        return self._bio

    @property
    def total_cash(self) -> int:
        """Get player's total cash."""
        return self._total_cash

    @property
    def round_cash(self) -> int:
        """Get player's round cash."""
        return self._round_cash

    @property
    def total_prizes(self) -> List[Prize]:
        """Get a copy of the list of player's prizes."""
        return [item for item in self._total_prizes]

    @property
    def round_prizes(self):
        """Returns copy to keep original list safe"""
        return [item for item in self._round_prizes]

    @property
    def total_score(self) -> int:
        """
        Returns the sum of the value of the total prizes and the total cash value.

        Does not include current round cash or prizes.
        """
        total = self.total_cash
        for prize in self._total_prizes:
            total += prize.value
        return total

    @property
    def total_round_score(self):
        """
        Returns the sum of the value of the round prizes and the round cash value.
        """
        total = self.round_cash
        for prize in self._round_prizes:
            total += prize.value
        return total

    @property
    def is_human(self):
        """Returns True if player is human."""
        return NotImplemented

    def ask_to_spin_solve_or_vowel(self, choices: List[str]):
        """Player returns a choice of whether to spin, solve or buy a vowel.
        
        Args:
            choices: List of valid choices the player can choose. The possible
            values are  'spin', 'vowel' and 'solve'.
        
        Returns:
            The player's choice: 'spin', 'vowel', or 'solve'
        """
        ...

    def buy_vowel(self) -> str:
        """Player returns a vowel guess."""
        ...

    def solve_puzzle(self) -> str:
        """Player returns a puzzle solution guess."""
        ...

    def guess_letter(self) -> str:
        """Player returns a consonant letter guess."""
        ...

    def add_cash(self, amount: int):
        """Adds amount to current round cash."""
        self._round_cash += amount

    def subtract_cash(self, amount: int):
        """Subtracts amount from current round cash."""
        self._round_cash -= amount

    def add_prize(self, prize: Prize):
        """Add prize to round prizes."""
        self._round_prizes.append(prize)

    def end_round_update(self, did_win: bool):
        """
        If did_win is True then add the current round cash/prizes to total.
        If False, discard the round cash/prizes.

        Resets round prizes/cash afterwards.
        """
        if did_win:
            self._total_prizes = self._total_prizes + self._round_prizes
            self._total_cash += self._round_cash

        # Reset round prizes/cash.
        self._round_prizes = []
        self._round_cash = 0


class Human(Player):
    """Human player class.
    
    Args:
        name: name of the player.
        bio: a short bio of the player.
    """

    def __init__(self, game_state, name: str = '', bio: str = ''):
        super().__init__(game_state, name, bio)
        self.draw_ui = game_state.draw_ui_function

    def __repr__(self):
        return f'Human({self.name!r}, {self.bio!r})'

    @property
    def is_human(self):
        """Returns True indicating this a Human instance."""
        return True

    def buy_vowel(self) -> str:
        """Request player input for a vowel to buy."""
        return self._get_input(VOWEL_GUESS_PARSERS).upper()

    def solve_puzzle(self) -> str:
        """Request player input for a puzzle to solve"""
        return self._get_input(SOLUTION_GUESS_PARSERS).upper().strip()

    def guess_letter(self) -> str:
        """Request player input for a letter to guess."""
        return self._get_input(CONSONANT_GUESS_PARSERS).upper()

    def ask_to_spin_solve_or_vowel(self, choices: List[str]) -> str:
        """Requests input from the player about whether they'd like to spin,
        buy a vowel, or solve the puzzle.
        
        Args:
            choices: List of valid choices the player can choose. The possible
            values are  'spin', 'vowel' and 'solve'.
        
        Returns:
            The player's choice: 'spin', 'vowel', or 'solve'
        """
        parsers = [spin_solve_vowel_parser_factory(choices)]
        answer = self._get_input(parsers)
        if 'spin' in answer.lower() and 'spin' in choices:
            return 'spin'
        elif 'vowel' in answer.lower() and 'vowel' in choices:
            return 'vowel'
        else:
            return 'solve'

    def _get_input(self, parsers_: List[Callable]) -> str:
        """
        Requests user input until input passes the parser requirements.
        Returns input string.
        """
        while error := _parse_input(input_string := input('>>> '), parsers_):
            self._game_state.update_input_error(error)
            self.draw_ui()

        self._game_state.clear_input_errors()
        return input_string.strip()


class Computer(Player):
    """Computer player class.
    
    Args:
        character: The character profile of the computer.
        difficulty: The difficulty level of the computer.
    """

    def __init__(self, game_state, character: Character, difficulty: int):
        super().__init__(game_state, character.name, character.bio)
        self._difficulty = difficulty
        
    def __repr__(self):
        return f'Computer(Character({self.name!r}, {self.bio!r}), {self.difficulty})'

    @property
    def difficulty(self) -> int:
        """Get computer difficulty."""
        return self._difficulty

    @property
    def is_human(self):
        """Returns False because this is a computer."""
        return False

    def ask_to_spin_solve_or_vowel(self, choices: List[str]) -> str:
        """Determine whether the computer wants to spin, solve, or buy a vowel."""
        if self._game_state.board.solved_percent > .75:
            return 'solve'
        elif 'vowel' in choices:
            if random.random() > .6:
                return 'vowel'
        else:
            return 'spin'


def generate_computer_players(game_state, difficulty: int) -> Tuple[Computer, Computer]:
    """Returns a tuple of two computer players with given difficulty and random
    character name/bios."""
    random.shuffle(Settings.CHARACTERS)
    computer1 = Computer(game_state, Settings.CHARACTERS[0], difficulty)
    computer2 = Computer(game_state, Settings.CHARACTERS[1], difficulty)
    return computer1, computer2


def _parse_input(string_: str, parsers_: List[Callable]) -> str or None:
    """
    Loops through parsers. If a parser returns an error, function will
    return that error as a string.
    Returns None if parsers found no error.
    """
    for parser in parsers_:
        if error := parser(string_):
            return error


EMPTY_PLAYER = Player('', '')
