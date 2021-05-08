from typing import Tuple, Callable, NamedTuple
import random
import players
import board
from wheel import Wheel
from settings import Settings



class Speech(NamedTuple):
    """
    Named tuple for storing dialogue information.

    Use instant=True if this dialogue will be displayed before input. No sleep
    delay will be applied after displaying this dialogue if instant is True.
    """
    speaker: str
    text: str
    input_displayed: bool = False

class GameState:
    """
    GameState keeps track of all the dynamic variables of the game.
    """

    def __init__(self):
        self._human = players.EMPTY_PLAYER
        self._computer1 = players.EMPTY_PLAYER
        self._computer2 = players.EMPTY_PLAYER
        self._current_player_number = 0
        self._board = board.EMPTY_BOARD
        self._wheel = Wheel()
        self._speech = Speech('', '', False)
        self._current_turn = 0
        self._current_round = 0
        self._is_round_active = False
        self._input_error = ''

    @property
    def human(self) -> players.Human:
        """Get human"""
        return self._human

    @property
    def computer1(self) -> players.Computer:
        """Get computer 1"""
        return self._computer1

    @property
    def computer2(self) -> players.Computer:
        """Get computer 2"""
        return self._computer2
    
    @property
    def current_player(self) -> players.Player:
        """Get current player"""
        num = self._current_player_number
        if num == 0:
            return self._human
        if num == 1:
            return self._computer1
        if num == 2:
            return self._computer2
        raise ValueError("Invalid current player number")
        
    @property
    def board(self) -> board.Board:
        """Get board"""
        return self._board
    
    @property
    def speech(self) -> Speech:
        """Get or set current speech."""
        return self._speech
    
    @speech.setter
    def speech(self, speech: Speech):
        self._speech = speech
    
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
    def input_error(self) -> str:
        """Get current input error"""
        return self._input_error
    
    def next_player(self):
        """Set current player to the next player."""
        self._current_player_number = (self._current_player_number + 1) % 3

    def create_human_player(self, human: players.Player):
        self._human = human

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
