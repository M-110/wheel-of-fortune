from src.wof.__main__ import WheelOfFortune, Speech
from src.wof.parsers import DIFFICULTY_PARSERS

wof = WheelOfFortune()

wof.show_speech(Speech("Pat", "Good evening everyone.", False))

wof.round()