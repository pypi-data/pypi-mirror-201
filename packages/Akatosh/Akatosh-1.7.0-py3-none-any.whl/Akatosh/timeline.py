from __future__ import annotations

from typing import TYPE_CHECKING, List, Union
from uuid import uuid4
import inspect

from .event import Event

if TYPE_CHECKING:
    from .actor import Actor


class Timeline:
    _id: int
    _time: Union[int, float]
    _actors: List[Actor]
    _events: List[Event]

    def __init__(self) -> None:
        """A class to represent a timeline in the simulation. Should not be instantiated directly."""
        self._id = uuid4().int
        self._time = 0
        self._actors = list()
        self._events = list()

    def schedule(self, actor: Actor):
        """Schedule an actor to the timeline.

        Args:
            actor (Actor): the actor to be scheduled.
        """
        event = Event(at=actor.time, priority=actor.priority, actor=actor)
        self.events.append(event)
        self.actors.append(actor)
        self.events.sort(key=lambda event: event.priority)
        self.events.sort(key=lambda event: event.at)
        if actor.scheduled is False:
            actor.status.append('scheduled')

    def forward(self, till: Union[int, float]):
        """Forward the timeline to a given time."""
        while True:
            if len(self.events) != 0:
                next_event = self.events.pop(0)
                if self.now < next_event.at:
                    self._time = next_event.at
                if next_event.at <= till:
                    try:
                        next(next_event.actor.perform())
                    except StopIteration:
                        pass
                else:
                    break
            else:
                break
            
    @property
    def now(self):
        """The current time of the timeline."""
        return self._time

    @property
    def actors(self):
        """The actors on the timeline."""
        return self._actors

    @property
    def events(self):
        """The events on the timeline."""
        return self._events
