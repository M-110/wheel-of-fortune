from typing import List, TYPE_CHECKING

GameState = "TypeHintFiller"
if TYPE_CHECKING:
    pass
    # from game_state import GameState


def draw_ui(game_state: GameState):
    """Print the UI."""
    print(_generate_game_ui_string(game_state))


def _generate_game_ui_string(game_state: GameState) -> str:
    """Generates the complete string which will be used as the UI."""
    return '\n'.join(_combine_puzzle_and_scoreboard_strings(game_state) +
                     _generate_dialogue_string(game_state) +
                     [game_state.input_error])


def _generate_puzzle_board_string(game_state: GameState) -> str:
    """Generates the portion of the UI string responsible for displaying
    the current board state and the category."""
    puzzle = game_state.board.masked_puzzle
    category = game_state.board.category
    puzzle_lines = _split_string_into_lines(puzzle)
    puzzle_lines = _vertically_center_lines(puzzle_lines)
    puzzle_lines = _horizontally_center_lines(puzzle_lines)
    return _generate_board_visuals(puzzle_lines, category)


def _split_string_into_lines(puzzle: str) -> List[str]:
    """Split string into rows of max length 12 using a recursive algorithm.
    This is used to fit the words to the width of the board."""
    if len(puzzle) < 13:
        return [puzzle]

    words = puzzle.split()
    for i in range(1, len(words)):
        substring_a, substring_b = ' '.join(words[:-i]), ' '.join(words[-i:])
        if len(substring_a) <= 12 and substring_b:
            return [substring_a] + _split_string_into_lines(substring_b)


def _vertically_center_lines(puzzle_lines: List[str]) -> List[str]:
    """A math equation used to guarantee there are 4 lines in the list and the
    lines containing strings are vertically centered."""
    length = len(puzzle_lines)
    prepend_lines = [''] * ((4 - length) // 2)
    append_lines = [''] * ((5 - length) // 2)
    return prepend_lines + puzzle_lines + append_lines


def _horizontally_center_lines(puzzle_lines: List[str]) -> List[str]:
    """
    Horizontally center each of the lines in the puzzle.
    """
    extra_space = min((12 - len(line)) // 2 for line in puzzle_lines)
    return [(' ' * extra_space + line).ljust(12) for line in puzzle_lines]


def _generate_board_visuals(puzzle_lines: List[str], category: str) -> str:
    """Insert each puzzle character and the category name into the puzzle board."""
    puzzle_string = ''.join(puzzle_lines)
    visual_string = \
        """    ╔═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗     ╔
    ║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║     ║
╔═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╗ ║
║   ║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║   ║ ╠
╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣ ║
║   ║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║   ║ ║
╚═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╝ ╠
    ║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║ {}║     ║
    ╚═══╬═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╬═══╝     ║
        ║{}║         ╚
        ╚═══════════════════════════════════════╝""" \
            .format(*(char + ' ' for char in puzzle_string), category.center(39))
    return visual_string


def _generate_scoreboard_string(game_state: GameState) -> str:
    """
    Generates a scoreboard that includes each player's name and cash.
    '♦' displayed next to the player whose turn it is.
    Displays round cash during rounds and total cash between rounds.
    """
    p1 = game_state.human.name
    p2 = game_state.computer1.name
    p3 = game_state.computer2.name
    turn = game_state._current_player_number
    if game_state.is_round_active:
        c1 = game_state.human.round_cash
        c2 = game_state.computer1.round_cash
        c3 = game_state.computer2.round_cash
    else:
        c1 = game_state.human.total_cash
        c2 = game_state.computer1.total_cash
        c3 = game_state.computer2.total_cash
    a1 = '♦' if turn == 0 else ' '
    a2 = '♦' if turn == 1 else ' '
    a3 = '♦' if turn == 2 else ' '
    scoreboard = \
        """═════════════════╗
 {} {}║
   ${}║
═════════════════╣
 {} {}║
   ${}║
═════════════════╣
 {} {}║
   ${}║
═════════════════╝
""" \
            .format(a1, p1.ljust(14), str(c1).ljust(13),
                    a2, p2.ljust(14), str(c2).ljust(13),
                    a3, p3.ljust(14), str(c3).ljust(13))
    return scoreboard


def _combine_puzzle_and_scoreboard_strings(game_state: GameState) -> List[str]:
    """Combines the puzzle board and the scoreboard together by zipping each line
    together."""
    puzzle = _generate_puzzle_board_string(game_state).split('\n')
    scoreboard = _generate_scoreboard_string(game_state).split('\n')
    return [''.join(list(pair)) for pair in zip(puzzle, scoreboard)]


def _generate_dialogue_string(game_state: GameState) -> List[str]:
    speaker = game_state.speech.speaker
    text = game_state.speech.text
    speaker_strings = _generate_speaker_string(speaker).split('\n')
    text_strings = _generate_dialogue_text_box(text).split('\n')
    return [''.join(list(pair)) for pair in zip(speaker_strings, text_strings)]


def _generate_speaker_string(speaker: str) -> str:
    """Generates the speaker part of the dialogue box and horizontally aligns
    the name of the speaker within that box."""
    return f""" ╔═══════════╦═
 ║{speaker.center(11)}║ 
 ╚═══════════╣ 
             ╚═"""


def _generate_dialogue_text_box(text: str) -> str:
    """Generates the text portion of the dialogue box."""
    line_1 = text
    line_2 = ''
    if len(text) > 60:
        word_list = text.split()
        for i in range(len(word_list) + 1):
            line = ' '.join(word for word in word_list[:i])
            if len(line) > 60:
                line_1 = ' '.join(word_list[:i - 1])
                line_2 = ' '.join(word_list[i - 1:])
                break
    return f"""═════════════════════════════════════════════════════════════╗
{line_1.ljust(61)}║
{line_2.ljust(61)}║
═════════════════════════════════════════════════════════════╝"""
