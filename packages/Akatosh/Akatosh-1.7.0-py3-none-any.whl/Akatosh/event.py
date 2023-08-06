from __future__ import annotations

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .actor import Actor


class Event:
    _at: Union[int, float]
    _priority: int
    _actor: Actor

    def __init__(self, at: Union[int, float], priority: int, actor: Actor) -> None:
        """A class to represent an event in the simulation. Should not be instantiated directly.

        Args:
            at (Union[int, float]): the time at which the event occurs.
            priority (int): the priority of the event.
            actor (Actor): the actor that the event is associated with.
        """
        self._at = at
        self._priority = priority
        self._actor = actor

    @property
    def at(self):
        """The time at which the event occurs."""
        return self._at

    @property
    def priority(self):
        """The priority of the event."""
        return self._priority

    @property
    def actor(self):
        """The actor that the event is associated with."""
        return self._actor
