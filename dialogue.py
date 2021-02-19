from settings import Settings
from typing import NamedTuple, TYPE_CHECKING
from time import sleep
import ui

GameState = "TypeHintFiller"
if TYPE_CHECKING:
    from game_state import GameState


class Speech(NamedTuple):
    """
    Named tuple for storing dialogue information.

    Use instant=True if this dialogue will be displayed before input. No sleep delay will be applied after displaying
    this dialogue if instant=True.
    """
    speaker: str
    text: str
    input_displayed: bool = False


class Dialogue:
    """
    Dialogue keeps track of the current speech, makes calls to update the UI, and calls sleep from the time module
    to give the player time to read the dialogue.

    game_state must be passed so that Dialogue can make calls to the print the current UI
    """

    def __init__(self, game_state: GameState):
        self._current_speech = Speech('', '', True)
        self.game_state = game_state

    @property
    def current_speech(self) -> Speech:
        """Get current speech"""
        return self._current_speech

    @property
    def current_text(self) -> str:
        """Get text component of speech"""
        return self.current_speech.text

    def new_speech(self, speech: Speech):
        """Set new speech. This will trigger a UI update"""
        self._current_speech = speech
        self.reveal_dialogue()

    def reveal_dialogue(self):
        """
        Updates the UI display with the new dialogue. If dialogue is not instant, this function will cause the game
        to sleep for a few seconds depending on the length of the text
        """
        ui.draw_ui(self.game_state)

        if self.current_speech.input_displayed:
            return

        calculated_wait = len(self.current_speech.text) / 9 * Settings.DIALOGUE_SPEED
        sleep(calculated_wait)
