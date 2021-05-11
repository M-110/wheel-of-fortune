import random
from collections import namedtuple
import csv
import json
from pathlib import Path

Character = namedtuple('Character', 'name bio')

Puzzle = namedtuple('Puzzle', 'category puzzle')

Wedge = namedtuple('Wedge', 'text type value')

Prize = namedtuple('Prize', 'name value')


def _import_characters():
    """Import characters from csv file in the data directory."""
    character_list = []
    with open(Path('data', 'characters.csv'), 'r', encoding='utf8') as file:
        csv_reader = csv.reader(file, delimiter='|')
        for character in csv_reader:
            character_list.append(Character(*character))
    return character_list


def _import_puzzles():
    """Import puzzles list from json file in the data directory."""
    puzzle_list = []
    with open(Path('data', 'puzzles.json'), 'r', encoding='utf8') as file:
        puzzles_dict = json.load(file)
    for category in puzzles_dict:
        for puzzle in puzzles_dict[category]:
            # Filter out puzzles shorter than 12 characters and puzzles that
            # are only 1 word long.
            if len(puzzle) > 12 and len(puzzle.split()) > 2:
                puzzle_list.append(Puzzle(category, puzzle))
    return puzzle_list


def _import_prizes():
    """Import prizes list from csv file in the data directory."""
    prize_list = []
    with open(Path('data', 'prizes.csv'), 'r', encoding='utf8') as file:
        csv_reader = csv.reader(file)
        for prize in csv_reader:
            prize_list.append(Prize(*prize))
    return prize_list


def _import_wheel_values():
    """Import wheel list and probabilities from text file"""
    wedge_list = []
    with open(Path('data', 'wheel.csv'), 'r', encoding='utf8') as file:
        csv_reader = csv.reader(file)
        for wedge in csv_reader:
            wedge_list.append(Wedge(*wedge))
    return wedge_list


def random_phrase(context: str) -> str:
    """Returns a random phrase that fits in the context"""
    return random.choice(PHRASE_DICT[context])


PHRASE_DICT = {'spin': ["I'd like to spin, Pat.",
                        "I think I'm gonna spin.",
                        "I'll spin",
                        "*spins the wheel*"],
               'solve': ["I'd like to solve the puzzle, Pat.",
                         "I think I'm gonna solve.",
                         "I'd like to solve."],
               'vowel': ["I'd like to buy a vowel please, Pat.",
                         "I'd like to buy a vowel.",
                         "Could I get a vowel, please?",
                         "I want to buy a vowel."],
               'bankrupt': ["Oh I'm sorry, looks like you've landed on BANKRUPT.",
                            "You've landed on BANKRUPT.",
                            "Uh oh, BANKRUPT.",
                            "Oh no, you've landed on BANKRUPT.",
                            "BANKRUPT!"],
               'lose_turn': ["LOSE A TURN.",
                             "Sorry, you landed on LOSE A TURN..",
                             'Uh oh, LOSE A TURN.'
                             "You've landed on LOSE A TURN."],
               'trip': ["You landed on a trip."],
               'duplicate_letter': ["No I'm sorry, '{}' has already been called.",
                                    "'{}' has already been called.",
                                    "Pay more attention, '{}' was already called.",
                                    "Sorry, '{}' was already guessed.",
                                    "'{}' was guessed already."],
               'failed_guess': ["There's' no '{}'.",
                                "Sorry, there is no '{}'.",
                                "Nope, tno '{}'.",
                                "'{}' is not there."],
               'correct_guess_single': ["Yep, there is {aan} '{letter}'.",
                                        "Yes, one '{letter}'.",
                                        "There's {aan} '{letter}'."],
               'correct_guess_multi': ["{count} '{letter}'.",
                                       "Yes, there are {count} '{letter}'.",
                                       "Yep, {count} '{letter}'.",
                                       "Wow, {count} '{letter}'."
                                       "We have {count} '{letter}'."],
               'correct_solve': ['Yep, you got it.',
                                 "Yep, that's it",
                                 'Well done, you got it.'
                                 "Wow, great job. That's correct.",
                                 "Yes, that is the answer."],
               'failed_solve': ["No, I'm sorry. That's not correct.",
                                "Nope, that is not the answer."
                                "No, not quite what we were looking for.",
                                "That is not correct.",
                                "That is not the answer."]}


class Settings:
    """Contains constants to be used during gameplay"""
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    MOST_COMMON_LETTERS = 'etaoinsrhldcumfpgwybvkxjqz'
    VOWELS = 'aeiou'
    CHARACTERS = _import_characters()
    PUZZLES = _import_puzzles()
    PRIZES = _import_prizes()
    WHEEL_VALUES = _import_wheel_values()
    BONUS_ROUND_VALUES = [3000] * 12 + [45000] * 4 + [50000] * 3 + [75000] * 2 + \
                         [100000]
    DIALOGUE_SPEED = 1
    random_phrase = random_phrase
