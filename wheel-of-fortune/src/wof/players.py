from typing import List, Tuple, Callable
from settings import Settings
from settings import Prize
from settings import Character
import random

from src.wof.board import Board
from src.wof.parsers import spin_solve_vowel_parser_factory

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

    def __init__(self, name: str, bio: str):
        self._name = name
        self._bio = bio
        self._total_cash = 0
        self._round_cash = 0
        self._total_prizes = []
        self._round_prizes = []
        
    def __repr__(self):
        return f'<{self.__class__.name} name={self.name}>'
    
    def __str__(self):
        return f'{self.name}:\n\ttotal cash: {self.total_cash}\n\tround_cash: {self.round_cash}'

    def ask_to_spin_solve_or_vowel(self, game_state, options: List[str]):
        ...
    
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
        """Returns true if player is human."""
        return False

    def add_cash(self, amount: int):
        """Adds amount to current round cash."""
        self._round_cash += amount

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

    def guess(self, board: Board):
        return "A"


class Human(Player):
    """Human player class.
    
    Args:
        name: name of the player.
        bio: a short bio of the player.
    """
    def __init__(self, draw_ui_callback: Callable,  name: str = '', bio: str = ''):
        super().__init__(name, bio)
        self.draw_ui = draw_ui_callback

    def __repr__(self):
        return f'Human({self.name!r}, {self.bio!r})'
    
    @property
    def is_human(self):
        return True

    def ask_to_spin_solve_or_vowel(self, game_state, choices: List[str]) -> str:
        parsers = [spin_solve_vowel_parser_factory(choices)]
        return self._get_input(game_state, parsers)

    def guess(self, guessed_letters: List[str], puzzle: str):
        pass
    
    def _get_input(self, game_state, parsers_: List[Callable]) -> str:
        """
        Requests user input until input passes the parser requirements.
        Returns input string.
        """
        while error := _parse_input(input_string := input('>>> '), parsers_):
            game_state.update_input_error(error)
            self.draw_ui()

        game_state.clear_input_errors()
        return input_string.strip()


class Computer(Player):
    """Computer player class.
    
    Args:
        character: The character profile of the computer.
        difficulty: The difficulty level of the computer.
    """
    def __init__(self, character: Character, difficulty: int):
        super().__init__(character.name, character.bio)
        self._difficulty = difficulty

    @property
    def difficulty(self) -> int:
        """Get computer difficulty."""
        return self._difficulty

    def __repr__(self):
        return f'Computer(Character({self.name!r}, {self.bio!r}), {self.difficulty})'

    def ask_to_spin_solve_or_vowel(self, game_state, choices: List[str]) -> str:
        """Determine whether the computer wants to spin, solve, or buy a vowel."""
        if game_state.board.solved_percent > .75:
            return 'solve'
        elif 'vowel' in choices:
            if random.random() > .6:
                return 'vowel'
        else:
            return 'spin'
                
        


def generate_computer_players(difficulty: int) -> Tuple[Computer, Computer]:
    """Returns a tuple of two computer players with given difficulty and random
    character name/bios."""
    random.shuffle(Settings.CHARACTERS)
    computer1 = Computer(Settings.CHARACTERS[0], difficulty)
    computer2 = Computer(Settings.CHARACTERS[1], difficulty)
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
