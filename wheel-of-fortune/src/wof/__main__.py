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
        self.game_state._human = players.Human(self.draw_ui)
        self.game_state.new_round()

    def create_computers(self):
        self.game_state.create_computer_players(5)
        self.game_state.generate_new_board()

    def show_speech(self, speech: Speech):
        self.game_state.speech = speech
        draw_ui(self.game_state)

    def draw_ui(self):
        draw_ui(self.game_state)
        
    def turn(self):
        # put this all in a while loop?
        choice = self.ask_player_round_choice()
        # if 'spin': spin = current_player.spin(), guess = current_player.guess()
        # if 'solve': solve_guess = current_player.solve
        # if 'vowel': subtract money, 

    def ask_player_round_choice(self) -> str:
        """Ask current player whether they want to spin, solve, or buy a vowel.
        
        Returns:
            'spin', 'solve', or 'vowels'
        """
        choices = ['solve']
        if self.game_state.board.vowels_remain \
                and self.game_state.current_player.round_cash >= 250:
            choices.append('spin')
            choices.append('vowels')
        elif self.game_state.board.letters_remain:
            choices.append('spin')
        self.show_speech(Speech('Pat', 'What would you like to do?'))
        return self.game_state.current_player.\
            ask_to_spin_solve_or_vowel(self.game_state, choices)

    def spin_wheel(self) -> Wedge:
        self.show_speech(Speech("", "Spinning the wheel...", False))
        return self.game_state._wheel.spin()
