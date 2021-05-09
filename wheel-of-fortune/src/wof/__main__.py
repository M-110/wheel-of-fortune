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
        
    def player_turn(self):
        continue_ = True
        while continue_:
            choice = self.ask_player_round_choice()
            
            if choice == 'solve':
                puzzle_guess = self.player_solve_puzzle()
                continue_ = self.check_puzzle_guess(puzzle_guess)
            elif choice == 'vowel':
                vowel = self.player_buy_vowel()
                continue_ = self.check_vowel_guess(vowel)
            elif choice == 'spin':
                wedge, continue_ = self.player_spin()
                if not continue_:
                    break
                letter = self.player_guess_letter()
                continue_ = self.check_letter_guess(letter)
                
                
                
                
    def player_solve_puzzle(self) -> str:
        guess = self.game_state.current_player.solve_puzzle(self.game_state)
        return guess
    
    def check_puzzle_guess(self, puzzle_guess: str) -> bool:
        pass
    
    def player_buy_vowel(self) -> str:
        vowel = self.game_state.current_player.buy_vowel(self.game_state)
        return vowel
    
    def check_vowel_guess(self, vowel_guess: str) -> bool:
        pass
        
    def player_spin(self) -> Tuple[Wedge, bool]:
        wedge = self.game_state.wheel.spin()
        return wedge, True
    
    def player_guess_letter(self) -> str:
        guess = self.game_state.current_player.guess_letter(self.game_state)
        return guess
    
    def check_letter_guess(self, letter: str) -> bool:
        ...

    def ask_player_round_choice(self) -> str:
        """Ask current player whether they want to spin, solve, or buy a vowel.
        
        Returns:
            'spin', 'solve', or 'vowels'
        """
        if not self.game_state.board.letters_remain:
            choices = ['solve']
        elif self.game_state.board.vowels_remain \
                and self.game_state.current_player.round_cash >= 250:
            choices = ['spin', 'solve', 'vowel']
        else:
            choices = ['spin', 'solve']
        
        self.show_speech(Speech('Pat', 'What would you like to do?'))
        return self.game_state.current_player.\
            ask_to_spin_solve_or_vowel(self.game_state, choices)

    def spin_wheel(self) -> Wedge:
        self.show_speech(Speech("", "Spinning the wheel...", False))
        return self.game_state._wheel.spin()
