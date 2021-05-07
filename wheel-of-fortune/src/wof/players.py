from typing import List, Tuple
from settings import Settings
from settings import Prize
from settings import Character
import random

from src.wof.board import Board

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
    def __init__(self, name: str, bio: str):
        super().__init__(name, bio)

    def __repr__(self):
        return f'Human({self.name!r}, {self.bio!r})'

    def guess(self, guessed_letters: List[str], puzzle: str):
        pass


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


def generate_computer_players(difficulty: int) -> Tuple[Computer, Computer]:
    """Returns a tuple of two computer players with given difficulty and random
    character name/bios."""
    random.shuffle(Settings.CHARACTERS)
    computer1 = Computer(Settings.CHARACTERS[0], difficulty)
    computer2 = Computer(Settings.CHARACTERS[1], difficulty)
    return computer1, computer2


EMPTY_PLAYER = Player('', '')
