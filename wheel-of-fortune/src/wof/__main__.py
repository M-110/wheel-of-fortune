from typing import NamedTuple, Callable, Tuple, List

from game_state import GameState, Speech
from parsers import LETTER_PARSERS
import players
from src.wof.settings import Wedge
from ui import draw_ui


class WheelOfFortune:
    """Main game class"""

    def __init__(self):
        self.game_state = GameState()
        self.create_players()

    def create_players(self):
        self.game_state.create_human_player(players.Human("Lyle", "Hi, my name is Lyle. I live in a tree."))
        self.game_state.create_computer_players(5)
        self.game_state.generate_new_board()

    def show_speech(self, speech: Speech):
        self.game_state.speech = speech
        draw_ui(self.game_state)

    def draw_ui(self):
        draw_ui(self.game_state)

    def get_input(self, parsers_: List[Callable]) -> str:
        """
        Requests user input until input passes the parser requirements.
        Returns input string.
        """
        while error := _parse_input(input_string := input('>>> '), parsers_):
            self.game_state.update_input_error(error)
            self.draw_ui()

        self.game_state.clear_input_errors()
        return input_string.strip()

    def ask_player_for_letter(self) -> str:
        if isinstance(self.game_state.current_player, players.Human):
            return self.get_input(LETTER_PARSERS)
        return self.game_state.current_player.guess(self.game_state.board)
    
    def spin_wheel(self) -> Wedge:
        self.show_speech(Speech("", "Spinning the wheel...", False))
        return self.game_state._wheel.spin()
    
        


def _parse_input(string_: str, parsers_: List[Callable]) -> str or None:
    """
    Loops through parsers. If a parser returns an error, function will
    return that error as a string.
    Returns None if parsers found no error.
    """
    for parser in parsers_:
        if error := parser(string_):
            return error
