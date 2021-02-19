import json
from collections import namedtuple

Character = namedtuple('Character', 'name bio')

Puzzle = namedtuple('Puzzle', 'category puzzle')

Wedge = namedtuple('Wedge', 'text type value')

Prize = namedtuple('Prize', 'name value')


def import_characters():
    """Import characters from text file"""
    character_list = []
    with open('settings/characters.txt', 'r', encoding='utf8') as file:
        for line in file:
            pair = line.split('|')
            pair[1] = pair[1].strip('\n').strip()
            character_list.append(Character(*pair))
    return character_list


def import_puzzles():
    """Import puzzles list from text file"""
    puzzle_list = []
    with open('settings/puzzles.json', 'r') as file:
        puzzles_dict = json.load(file)
    for category in puzzles_dict:
        for puzzle in puzzles_dict[category]:
            if len(puzzle) > 12 and len(puzzle.split()) > 2:
                puzzle_list.append(Puzzle(category, puzzle))
    return puzzle_list


def import_prizes():
    """Import prizes list from text file"""
    prize_list = []
    with open('settings/prizes.txt', 'r') as file:
        for line in file:
            prize_list.append(Prize(*line.strip('\n').split(',')))
    return prize_list


def import_wheel_values():
    """Import wheel list and probabilities from text file"""
    wedge_list = []
    with open('settings/wheel.txt', 'r') as file:
        for line in file:
            wedge_list.append(Wedge(*line.strip('\n').replace(' ', '').split(',')))
    return wedge_list


def import_bonus_round_values():
    """Import bonus round values from text file"""
    bonus_list = []
    with open('settings/bonus_round.txt', 'r') as file:
        for line in file:
            bonus_list.append(line.strip('\n'))
    return bonus_list


class Settings:
    """Contains constants to be used during gameplay"""
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    MOST_COMMON_LETTERS = 'etaoinsrhldcumfpgwybvkxjqz'
    VOWELS = 'aeiou'
    CHARACTERS = import_characters()
    PUZZLES = import_puzzles()
    PRIZES = import_prizes()
    WHEEL_VALUES = import_wheel_values()
    BONUS_ROUND_VALUES = import_bonus_round_values()
    DIALOGUE_SPEED = .2
