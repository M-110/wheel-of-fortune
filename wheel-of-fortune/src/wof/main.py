import time
from typing import NamedTuple, Callable, Tuple, List

from game_state import GameState, Speech
from parsers import LETTER_PARSERS, a_or_an
import players
from src.wof.settings import Wedge, Settings
from ui import draw_ui


class WheelOfFortune:
    """Main game class"""

    def __init__(self):
        self.game_state = GameState()
        self.draw_ui = self.game_state.draw_ui_function
        self.game_state._human = players.Human(self.game_state, 'Lyle')
        self.game_state.new_round()

    def create_computers(self):
        """Add computers to the game_state and generate a new board."""
        self.game_state.create_computer_players(5)
        self.game_state.generate_new_board()

    def show_speech(self, name, text, input_displayed=False, delay=True):
        """
        Display the name and text in the dialogue box of the UI. This will
        trigger the display to refresh.
        
        If input_displayed is True, the UI display will be one line shorter as
        to provide room for the user input.
        
        If delay is True, there will be time delay based on the length of the
        word count of the text.
        """
        self.game_state.speech = Speech(name, text, input_displayed, delay)
        # draw_ui(self.game_state)

    def round(self):
        """"""
        self.game_state.start_round()
        while self.player_turn():
            self.game_state.next_player()
        self.game_state.end_round()
        self.game_state.current_player.update_at_round_end(True)
        for player in self.game_state.inactive_players:
            player.update_at_round_end(False)
        self.show_speech('Pat',
                         Settings.get_random_phrase('round_winner')
                         .format(name=self.game_state.current_player.name,
                                 cash=self.game_state.current_player.total_score),
                         delay=False)
        time.sleep(3)

    def player_turn(self) -> bool:
        """
        Initiates a turn loop for the current player which repeats the process
        of spinning, guessing and solving until either the player has correctly
        solved the the puzzle, they've gotten "bankrupt" or "lose a turn" from
        spinning, or they've incorrectly guessed a letter.
        
        Returns False if puzzle has been solved and round is over.
        Returns True if player lost their turn."""
        continue_ = True
        print(self.game_state.board.puzzle_answer)
        while continue_:
            choice = self.ask_player_round_choice()
            if choice == 'solve':
                puzzle_guess = self.player_solve_puzzle()
                continue_ = self.check_puzzle_guess(puzzle_guess)
                if not continue_:
                    break
                self.reveal_puzzle()
                return False
            elif choice == 'vowel':
                self.game_state.current_player.subtract_cash(250)
                vowel = self.player_buy_vowel()
                continue_ = self.check_letter_guess(vowel)
                if not continue_:
                    break
                self.reveal_letter(vowel)
            elif choice == 'spin':
                wedge, continue_ = self.player_spin()
                if not continue_:
                    break
                letter = self.player_guess_letter()
                continue_ = self.check_letter_guess(letter)
                if not continue_:
                    break
                self.reveal_letter(letter)
                self.reward_letter(letter, wedge)
        return False

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

        if self.game_state.current_player.is_human:
            if len(choices) == 2:
                choice_text = ' or '.join(choices)
            elif len(choices) == 3:
                choice_text = f'{choices[0]}, {choices[1]}, or {choices[2]}'
            else:
                return 'solve'
            choice_text = choice_text.replace('vowel', 'buy a vowel')
            self.show_speech('',
                             f'Would you like to {choice_text}?',
                             input_displayed=True,
                             delay=False)

        answer = self.game_state.current_player. \
            ask_to_spin_solve_or_vowel(choices)
        self.show_speech(self.game_state.current_player.name,
                         Settings.get_random_phrase(answer))
        return answer

    def player_solve_puzzle(self) -> str:
        if self.game_state.current_player.is_human:
            self.show_speech('',
                             'What is the answer to the puzzle?',
                             input_displayed=True,
                             delay=False)
        guess = self.game_state.current_player.solve_puzzle()
        self.show_speech(self.game_state.current_player.name, guess)
        return guess

    def check_puzzle_guess(self, puzzle_guess: str) -> bool:
        """Returns True if the puzzle guess is correct."""
        is_correct = self.game_state.board.check_if_puzzle_guess_is_right(puzzle_guess)

        if is_correct:
            self.show_speech('Pat', Settings.get_random_phrase('correct_solve'))
        else:
            self.show_speech('Pat', Settings.get_random_phrase('failed_solve'))
        return is_correct

    def player_buy_vowel(self) -> str:
        if self.game_state.current_player.is_human:
            self.show_speech('',
                             'What vowel would you like to buy?',
                             input_displayed=True,
                             delay=False)

        vowel = self.game_state.current_player.buy_vowel()
        self.show_speech(self.game_state.current_player.name,
                         f"I'd like to buy {a_or_an(vowel)} '{vowel}'")
        return vowel

    def player_spin(self) -> Tuple[Wedge, bool]:
        self.show_speech('', '*Spinning the wheel*')
        wedge = self.game_state.wheel.spin()

        if wedge.value in ['bankrupt', 'lose_turn']:
            self.show_speech('Pat', Settings.get_random_phrase(wedge.value))
            return wedge, False
        elif wedge.value == 'trip':
            self.show_speech('Pat', Settings.get_random_phrase('trip'))
            return wedge, True
        else:
            self.show_speech('Pat', f"You landed on {wedge.text}")
            return wedge, True

    def player_guess_letter(self) -> str:
        if self.game_state.current_player.is_human:
            self.show_speech('',
                             'What letter would you like to guess?',
                             input_displayed=True,
                             delay=False)
        guess = self.game_state.current_player.guess_letter()
        self.show_speech(self.game_state.current_player.name,
                         f"I'd like to guess {a_or_an(guess)} '{guess}'")
        return guess

    def check_letter_guess(self, letter: str) -> bool:
        if letter in self.game_state.board.guessed_letters:
            self.show_speech('Pat',
                             Settings.get_random_phrase('duplicate_letter')
                             .format(letter))
            return False
        elif letter not in self.game_state.board.puzzle_answer:
            self.show_speech('Pat',
                             Settings.get_random_phrase('failed_guess')
                             .format(letter))
            return False
        else:
            count = self.game_state.board.get_letter_count_in_puzzle(letter)
            if count == 1:
                self.show_speech('Pat',
                                 Settings.get_random_phrase('correct_guess_single')
                                 .format(aan=a_or_an(letter), letter=letter))
            else:
                self.show_speech('Pat',
                                 Settings.get_random_phrase('correct_guess_multi')
                                 .format(count=count,
                                         letter=letter + 's'))
        return letter in self.game_state.board.puzzle_answer

    def reveal_letter(self, letter: str):
        """Slowly reveal the guessed letter on the board"""
        board = self.game_state.board

        # Highlight all occurrences of the letter before revealing
        for i, char in enumerate(board.puzzle_answer):
            if char == letter:
                board.puzzle_answer = board.puzzle_answer[:i] + '░' + \
                                      board.puzzle_answer[i + 1:]
                self.draw_ui()
                time.sleep(1)
        time.sleep(1)

        # Replace the highlight with the actual letter
        board.puzzle_answer = board.puzzle_answer.replace('░', letter)
        board.add_guess(letter)
        self.draw_ui()

    def reward_letter(self, letter: str, wedge: Wedge):
        """Apply the correct round cash to the current player."""
        if wedge.type == "cash":
            letter_count = self.game_state.board.get_letter_count_in_puzzle(letter)
            print(f'Adding {int(wedge.value) * letter_count} dollars.')
            self.game_state.current_player.add_cash(int(wedge.value) * letter_count)
        elif wedge.type == "trip":
            self.game_state.current_player.add_prize(wedge.value)

    def reveal_puzzle(self):
        """Reveal the full puzzle, display the winner of the round, and pause
        for 3 seconds."""
        self.game_state.board.reveal()
        self.show_speech('',
                         f'{self.game_state.current_player.name} wins the round.',
                         delay=False)
        time.sleep(3)

    def reward_puzzle(self):
        self.game_state
