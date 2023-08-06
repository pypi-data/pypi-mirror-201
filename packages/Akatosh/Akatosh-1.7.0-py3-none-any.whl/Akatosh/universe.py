from ctypes import Union
from math import inf
from typing import List, Union
from uuid import uuid4

from .timeline import Timeline


class Universe:
    _id: int
    _timeline: Timeline
    _accuracy: int
    _till: Union[int, float]

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Universe, cls).__new__(cls)
        return cls.instance

    def __init__(self, accuracy:int=3) -> None:
        """The universe in which the simulation takes place. Should not be instantiated directly."""
        self._id = uuid4().int
        self._timeline = Timeline()
        self._till = int()
        self._accuracy = accuracy

    def simulate(self, till: Union[int, float] = inf) -> None:
        """Simulate the universe to a given time."""
        self._till = till
        while self.timeline.now <= self.till:
            self.timeline.forward(self.till)
            if len(self.timeline.events) == 0:
                break

    @property
    def timeline(self) -> Timeline:
        """The timeline of the universe."""
        return self._timeline

    @property
    def till(self) -> Union[int, float]:
        """The time to which the universe is simulated."""
        return self._till

    @property
    def now(self) -> Union[int, float]:
        """The current time of the universe."""
        return self.timeline.now
    
    @property
    def accuracy(self) -> int:
        """The accuracy of the universe in term of minimum time step. e.g., 3 means 0.001s."""
        return self._accuracy

    @accuracy.setter
    def accuracy(self, value: int) -> None:
        self._accuracy = value

Mundus = Universe()
