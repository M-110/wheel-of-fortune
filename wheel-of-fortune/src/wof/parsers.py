from typing import Callable, Union, List


def len_range_parser_factory(min_len: int = 0, max_len: int = 100) -> Callable:
    """
    Returns a function which takes a string as input and returns
    an error if string length is outside of specified range.
    Min and max are inclusive.
    """
    if min_len > max_len:
        raise ValueError('Invalid range. min_len cannot be less than max_len')
    elif min_len < 0 or max_len < 0:
        raise ValueError('Invalid range. min and max cannot be negative')

    def len_range(string: str) -> Union[str, None]:
        """Returns error if string length outside of specified range"""
        if min_len == max_len:
            if len(string) != min_len:
                return f'Input must be {min_len} character{"" if min_len == 1 else "s"} long'
        elif len(string) < min_len:
            return f'Input must be at least {min_len} character{"" if min_len == 1 else "s"} long'
        elif len(string) > max_len:
            return f'Input cannot be more than {max_len} character{"" if max_len == 1 else "s"} long'

    return len_range


def num_range_parser_factory(min_num: int = 1, max_num: int = 10) -> Callable:
    """
    Returns a function which takes a string as input and returns
    an error if the number is outside of the specified range.
    Min and max are inclusive.
    """
    if min_num > max_num:
        raise ValueError('Invalid range. min_num cannot be less than max_num')

    def num_range(string: str) -> Union[str, None]:
        """Returns error if int(string) is outside of specified range"""
        try:
            num = int(string)
        except ValueError:
            return f'Input must be an integer in range {min_num} - {max_num}'

        if not (min_num <= num <= max_num):
            return f'Input must be in range {min_num} - {max_num}'

    return num_range


def alphanumeric_parser_factory(alpha=True, num=True) -> Callable:
    """
    Returns a function which takes a string as input
    and returns whether it is alpha, numeric, or alphanumeric
    depending on alpha and num parameters
    """
    if not (alpha or num):
        raise AttributeError('alpha and num are both False. At least one must be true')

    def alphanumeric(string_: str) -> Union[str, None]:
        """
        Returns error string if string_ is not alphabetical, alphanumeric, or alphanumeric
        depending on the created parameters.
        """
        string_ = string_.replace(' ', '')
        if alpha and num:
            if not string_.isalnum():
                return 'Input must be be alphanumeric.'
        elif alpha:
            if not string_.isalpha():
                return 'Input must be alphabetical'
        else:
            if not string_.isnumeric():
                return 'Input must be a number'

    return alphanumeric


def spin_solve_vowel_parser_factory(options: List[str]) -> Callable:
    """
    Returns a function which takes a string as input and returns whether any
    of the options are in it.
    """
    if len(options) == 1:
        option_string = options[0]
    elif len(options) == 2:
        option_string = ' or '.join(options)
    else:
        option_string = f'{options[0]}, {options[1]}, or {options[2]}'

    def spin_solve_vowel_parser(string_: str) -> Union[str, None]:
        """Returns error string if string_ does not contain spin, solve, or vowel."""
        if all(choice not in string_.lower() for choice in options):
            return f'Input must include {option_string}'

    return spin_solve_vowel_parser


def consonant_parser(string_: str) -> Union[str, None]:
    """Returns error if string is not a consonant."""
    if string_.lower() not in 'bcdfghjklmnpqrstvwxyz':
        return 'Input must be a consonant'
    
    
def vowel_parser(string_: str) -> Union[str, None]:
    """Returns error if string is not a vowel."""
    if string_.lower() not in 'aeiou':
        return 'Input must be a vowel'


def a_or_an(string_: str):
    if string_.lower() in 'bcdgjkpqtuvwyz':
        return 'a'
    else:
        return 'an'


NAME_PARSERS = [len_range_parser_factory(2, 12),
                alphanumeric_parser_factory(alpha=True, num=False)]

BIO_PARSERS = [len_range_parser_factory(2, 200)]

DIFFICULTY_PARSERS = [num_range_parser_factory(1, 10)]

LETTER_PARSERS = [len_range_parser_factory(1, 1),
                  alphanumeric_parser_factory(alpha=True, num=False)]

CONSONANT_GUESS_PARSERS = [len_range_parser_factory(1, 1),
                           consonant_parser]

VOWEL_GUESS_PARSERS = [len_range_parser_factory(1, 1),
                           vowel_parser]

SOLUTION_GUESS_PARSERS = [len_range_parser_factory(1, 60)]
