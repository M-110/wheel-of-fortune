from typing import Tuple, Callable
import random

import ui
from player_input import get_input, parsers
from game_state import players
from game_state import GameState
from game_state import Settings


def run_game():
    pass


def game_cycle():
    game_state = setup_game()
    intro()
    toss_up(game_state, 1000)
    toss_up(game_state, 2000)
    puzzle_round(game_state, 1)
    commercial()
    # round(2) Mystery
    # *Commercial*
    # round(3) express, prize puzzle
    # *Commercial*
    # toss_up(triple)
    # round(4)
    # *Commercial*
    # bonus_round
    # *promotion_plug*
    # *post_game_chat*


def setup_game() -> GameState:
    """
    Setup initial game state.
    """
    ui.dialogue('Python', "Welcome to the Wheel of Fortune for Python!")
    ui.dialogue('Python', "Let's setup your game.")
    ui.dialogue('Python', "What would you like your name to be?")
    player_name = get_input(name_parsers)
    ui.dialogue('Python', "How would you like to introduce yourself? (name, where you're from, etc.)")
    player_bio = get_input(bio_parsers)
    ui.dialogue('Python', "What difficulty would you like your opponents to be? (1-10)")
    difficulty = get_input(difficulty_parsers)
    ui.dialogue('Python', 'Generating your fellow contestants...')
    human = players.Human(player_name, player_bio)
    computer1, computer2 = generate_computer_players(int(difficulty))
    return GameState(human, computer1, computer2)


def generate_computer_players(difficulty: int) -> Tuple[players.Computer, ...]:
    """returns two computer players with given difficulty and random character name/bios"""
    random.shuffle(Settings.CHARACTERS)
    computer1 = players.Computer(Settings.CHARACTERS[0], difficulty)
    computer2 = players.Computer(Settings.CHARACTERS[1], difficulty)
    return computer1, computer2


def intro():
    """Just some opening dialogue"""
    ui.dialogue('Announcer', "From Sony Picture's studio, it's America's game.")
    ui.dialogue('Audience', 'Wheel. Of. FORTUNE! *applause*')
    ui.dialogue('Announcer', "Ladies and gentlemen, here are the stars of our show. Pat Sajak and Vanna White.")
    ui.dialogue('Crowd', "*applause*")
    ui.dialogue('Pat', 'Thank you Jim. Thanks everybody. Another nice crowd, we appreciate that.')
    ui.dialogue('Pat', "Alright, we'd like to get you some money so let's get started.")


def toss_up(game_state: GameState, cash_reward: int):
    pass


def puzzle_round(game_state: GameState, round_number: int):
    game_state.new_round()


def commercial():
    pass


# region Parsers:
name_parsers = (parsers.len_range_parser_factory(2, 12),
                parsers.alphanumeric_parser_factory(alpha=True, num=False))

bio_parsers = (parsers.len_range_parser_factory(2, 200),)

difficulty_parsers = (parsers.num_range_parser_factory(1, 10),)
# endregion

# game_cycle()

## Test:
player1 = players.Human('Warrior 1', 'A veteran of the great battle of Katabatic.')
computer1, computer2 = generate_computer_players(5)
game_state = GameState(player1, computer1, computer2)

puzzle_round(game_state, 0)
