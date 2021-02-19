from typing import Callable, Tuple, TYPE_CHECKING
import ui
GameState = "TypeHintFiller"
if TYPE_CHECKING:
    from game_state import GameState


def get_input(game_state: GameState, parsers_: Tuple[Callable, ...]) -> str:
    """
    Requests user input until input passes the parser requirements.
    Returns input string.
    """
    while error := _parse_input(input_string := input('>>> '), parsers_):
        game_state.update_input_error(error)
        ui.draw_ui(game_state)

    game_state.clear_input_errors()
    return input_string.strip()


def _parse_input(string_: str, parsers_: Tuple[Callable, ...]) -> str or None:
    """
    Loops through parsers. If a parser returns an error, function will
    return that error as a string.
    Returns None if parsers found no error.
    """
    for parser in parsers_:
        if error := parser(string_):
            return error
