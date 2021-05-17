import random
from typing import List

from settings import Settings
from settings import Wedge


class Wheel:
    """
    Simulates the wheel and contains a list of wedges that come from the
    settings.
    
    This class is used for the spin method which will randomly return one of the
    wedges from the wheel.
    """
    def __init__(self):
        self._wedges = Settings.WHEEL_VALUES

    @property
    def wedges(self) -> List[Wedge]:
        """Get a list of all wedges on the wheel."""
        return self._wedges

    def spin(self) -> Wedge:
        """Returns random wedge from list of wheel values."""
        return random.choice(self.wedges)
