from typing import Tuple, Callable
import random
import players
import board
from wheel import Wheel
from settings import Settings
from dialogue import Dialogue


class GameState:
    """
    GameState keeps track of all the dynamic variables of the game.
    """

    def __init__(self):
        self._player = players.EMPTY_PLAYER
        self._computer1 = players.EMPTY_PLAYER
        self._computer2 = players.EMPTY_PLAYER
        self._board = board.empty_board
        self._wheel = Wheel()
        self._current_turn = 0
        self._current_round = 0
        self._is_round_active = False
        self._dialogue = Dialogue(self)
        self._input_error = ''

    # region Properties
    @property
    def player(self) -> players.Human:
        """Get player"""
        return self._player

    @property
    def computer1(self) -> players.Computer:
        """Get computer 1"""
        return self._computer1

    @property
    def computer2(self) -> players.Computer:
        """Get computer 2"""
        return self._computer2

    @property
    def board(self) -> board.Board:
        """Get board"""
        return self._board

    @property
    def current_turn(self) -> int:
        """Get current turn"""
        return self._current_turn

    @property
    def current_round(self) -> int:
        """Get current round"""
        return self._current_round

    @property
    def is_round_active(self) -> bool:
        """Get is_round_active"""
        return self._is_round_active

    @property
    def dialogue(self) -> Dialogue:
        """Get dialogue object"""
        return self._dialogue

    @property
    def input_error(self) -> str:
        """Get current input error"""
        return self._input_error

    # endregion

    def create_human_player(self, human: players.Player):
        self._player = human

    def create_computer_players(self, difficulty: int):
        (self._computer1, self._computer2) = players.generate_computer_players(difficulty)

    def update_input_error(self, error: str):
        """Updates the input_error string"""
        self._input_error = f" ### Error: Invalid input. {error}."

    def clear_input_errors(self):
        self._input_error = ''

    def generate_new_board(self):
        """Get a random new puzzle and create a new board with this puzzle"""
        random_puzzle = random.choice(Settings.PUZZLES)
        self._board = board.Board(random_puzzle)

    def new_round(self):
        """Start a new round"""
        self.generate_new_board()
