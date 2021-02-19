from typing import List, Tuple
from settings import Settings
from settings import Prize
from settings import Character
import random

ALPHABET = Settings.ALPHABET
VOWELS = Settings.VOWELS
MOST_COMMON_LETTERS = Settings.MOST_COMMON_LETTERS


class Player:
    """
    Base class for players
    """

    def __init__(self):
        self._name = ''
        self._bio = ''
        self._total_cash = 0
        self._round_cash = 0
        self._total_prizes = []
        self._round_prizes = []
        self._was_introduced = False

    def __str__(self):
        return f'{self.name}:\n\ttotal cash: {self.total_cash}\n\tround_cash: {self.round_cash}'

    @property
    def name(self):
        return self._name

    @property
    def bio(self):
        return self._bio

    @property
    def was_introduced(self):
        return self._was_introduced

    @property
    def total_cash(self):
        return self._total_cash

    @property
    def round_cash(self):
        return self._round_cash

    @property
    def total_prizes(self):
        """Returns copy to keep original list safe"""
        return [item for item in self._total_prizes]

    @property
    def round_prizes(self):
        """Returns copy to keep original list safe"""
        return [item for item in self._round_prizes]

    def get_total_score(self) -> int:
        """
        Returns the sum of the value of the total prizes and the total cash value.

        Does not include current round cash or prizes.

        :return: int: total score
        """
        total = self.total_cash
        for prize in self._total_prizes:
            total += prize.value
        return total

    def get_round_score(self):
        """
        Returns the sum of the value of the round prizes and the round cash value.

        :return: int: round score
        """
        total = self.round_cash
        for prize in self._round_prizes:
            total += prize.value
        return total

    def add_cash(self, amount: int):
        """
        Adds amount to current round cash
        """
        self._round_cash += amount

    def add_prize(self, prize: Prize):
        """
        Add prize to round prizes
        """
        self._round_prizes.append(prize)

    def reset_round_values(self):
        """
        Resets the round prizes and cash bash to empty/0
        """
        self._round_prizes = []
        self._round_cash = 0

    def end_round_update(self, did_win):
        """
        If did_win == True the round prizes/cash will be added to total.
        Otherwise round prizes/cash will just be discarded.

        Resets round prizes/cash to empty/0 afterwards
        """
        if did_win:
            self._total_prizes = self._total_prizes + self._round_prizes
            self._total_cash += self._round_cash
        self.reset_round_values()


class Human(Player):
    def __init__(self, name: str, bio: str):
        super().__init__()
        self._name = name
        self._bio = bio

    def __repr__(self):
        return f'Human({self.name!r}, {self.bio!r})'

    def guess(self, guessed_letters: List[str], puzzle: str):
        pass


class Computer(Player):
    def __init__(self, character: Character, difficulty: int):
        super().__init__()
        self._name = character.name
        self._bio = character.bio
        self._difficulty = difficulty

    @property
    def difficulty(self):
        """Get computer difficulty"""
        return self._difficulty

    def __repr__(self):
        return f'Computer(Character({self.name!r}, {self.bio!r}), {self.difficulty})'

    def guess(self, guessed_letters: List[str], puzzle: str):
        pass


def generate_computer_players(difficulty: int) -> Tuple[Computer, ...]:
    """returns two computer players with given difficulty and random character name/bios"""
    random.shuffle(Settings.CHARACTERS)
    computer1 = Computer(Settings.CHARACTERS[0], difficulty)
    computer2 = Computer(Settings.CHARACTERS[1], difficulty)
    return computer1, computer2


EMPTY_PLAYER = Player()
