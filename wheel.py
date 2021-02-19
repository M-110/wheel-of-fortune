from settings import Settings
from settings import Wedge
import random


class Wheel:
    """
    Wheel Class!! Ya!
    """

    def __init__(self):
        self._wedges = Settings.WHEEL_VALUES

    @property
    def wedges(self):
        return self._wedges

    def spin(self) -> Wedge:
        """
        Returns random wedge from list of wheel values

        :returns: Wedge: Wedge(text, type, value)
        """
        return random.choice(self.wedges)