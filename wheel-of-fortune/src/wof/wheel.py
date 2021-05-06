import random
from typing import List

from settings import Settings
from settings import Wedge


class Wheel:
    """
    Wheel Class!! Ya!
    """
    def __init__(self):
        self._wedges = Settings.WHEEL_VALUES

    @property
    def wedges(self) -> List[Wedge]:
        return self._wedges

    def spin(self) -> Wedge:
        """Returns random wedge from list of wheel values."""
        return random.choice(self.wedges)