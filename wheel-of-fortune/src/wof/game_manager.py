from typing import Tuple, Callable

# from dialogue import Speech
# from game_state import GameState
# import player_input
# import parsers
# import ui
import players
from players import Player

SKIP = True

class GameManager:
    def __init__(self):
        self.game_state = GameState()
        self.game_cycle()

    def game_cycle(self):
        if SKIP:
            self.debug_setup()
        else:
            self.setup_sequence()
            self.show_intro()
        self.new_round_setup()
        self.game_state.board._guessed_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L']
        self.display_speech('BABYCAT', 'OH NO IM JUST A BABY CAt, HOW DID I GET ON WHEEL O F FORTUNERT? HA! ? I DUNNO')
        self.turn(self.game_state.computer1)

    def setup_sequence(self):
        self.display_speech('Python', 'Welcome to the Wheel of Fortune for Python!')
        self.display_speech('Python', "Let's setup your game.")

        player_name = self.get_input_with_speech('Python', 'What would you like your name to be?', parsers.NAME_PARSERS)
        player_bio = self.get_input_with_speech('Python', "How would you like to introduce yourself? (name, where "
                                                          "you're from, etc.)", parsers.BIO_PARSERS)
        difficulty = self.get_input_with_speech('Python', 'What difficulty would you like your opponents to be? (1-10)',
                                                parsers.DIFFICULTY_PARSERS)

        self.display_speech('Python', "Generating your fellow contestants...")

        self.game_state.create_human_player(players.Human(player_name, player_bio))
        self.game_state.create_computer_players(int(difficulty))

        self.display_speech('Python', 'Beginning your game...')

    def debug_setup(self):
        self.game_state.create_human_player(players.Human('human', 'hi im human'))
        self.game_state.create_computer_players(5)

    def show_intro(self):
        self.display_speech('Announcer', "From Sony Picture's studio, it's America's game.")
        self.display_speech('Audience', 'Wheel. Of. FORTUNE! *applause*')
        self.display_speech('Announcer', "Ladies and gentlemen, here are the stars of our show. Pat Sajak and Vanna "
                                         "White.")
        self.display_speech('Crowd', "*applause*")
        self.display_speech('Pat', 'Thank you Jim. Thanks everybody. Another nice crowd, we appreciate that.')
        self.display_speech('Pat', "Alright, we'd like to get you some money so let's get started.")

    def new_round_setup(self):
        self.game_state.generate_new_board()

    def turn(self, player: Player):
        self.display_speech('Pat', f"Alright, it's your turn, {player.name} ")

    def display_speech(self, speaker: str, text: str):
        self.game_state.dialogue.new_speech(Speech(speaker, text))

    def get_input_with_speech(self, speaker: str, text: str, parsers_: Tuple[Callable, ...]) -> str:
        self.game_state.dialogue.new_speech(Speech(speaker, text, input_displayed=True))
        return player_input.get_input(self.game_state, parsers_)