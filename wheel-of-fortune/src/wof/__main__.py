from typing import NamedTuple

from game_state import GameState, Speech
from ui import draw_ui




class WheelOfFortune:
    """Main game class"""
    def __init__(self):
        self.game_state = GameState()
        
    def _show_speech(self, speech: Speech):
        self.game_state.speech = speech
        draw_ui(self.game_state)
