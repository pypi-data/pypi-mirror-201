from __future__ import annotations
from typing import Generator, List, Optional, Union, Callable, TYPE_CHECKING
from uuid import uuid4
from math import inf
import warnings

from Akatosh import Mundus

if TYPE_CHECKING:
    from .resource import Resource
    from .producer import Producer
    from .timeline import Timeline


class Actor:
    def __init__(
        self,
        action: Optional[Callable] = None,
        at: Union[int, float, Callable] = 0,
        step: Optional[int | float | Callable] = None,
        till: Optional[int | float | Callable] = None,
        after: Optional[Actor | List[Actor]] = None,
        priority: int = 0,
        active: bool = True,
        label: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Create an actor, aka event. if step and till are both None, the actor is non-continuous and one time only. If a till is defined, then step can not be non. The arguments "at", "step" and "till" accepts int, float or callable. If callable, the function must return a int or float. If the callable returns a float, the float will be rounded to the current accuracy of Mundus.

        Args:
            action (Optional[Callable], optional): the function that will happens. Defaults to None only if this is not a subclass of Actor.
            at (Union[int, float, Callable], optional): when the event starts. Defaults to 0.
            step (Optional[int  |  float  |  Callable], optional): next time the event starts. Defaults to None.
            till (Optional[int  |  float  |  Callable], optional): when the event stops. Defaults to None.
            after (Optional[Actor  |  List[Actor]], optional): whether the event should happens only if other event(s) happened. Defaults to None.
            priority (int, optional): the priority of this actor/event. Defaults to 0.
            active (bool, optional): whether the event should be active directly. Defaults to True. If false, the actor must call activate() to activate the actor.
            label (Optional[str], optional): a short description for this event. Defaults to None.
        """

        # generate a unique id for this actor
        self._id = uuid4().int

        # assign the label to this actor
        self._label = label or str()

        # assign the action to this actor
        self._action = action

        # assign the timeline to this actor
        self._timeline = Mundus.timeline

        self.timeline.actors.append(self)

        # assign the priority to this actor
        self._priority = priority

        # pass the action parameters
        self._kwargs = kwargs

        # initialize the follower list
        self._followers: List[Actor] = list()

        # assign the waiting target to this actor
        if after is not None:
            if isinstance(after, Actor):
                self._after = [after]
                after.followers.append(self)
                if after.priority > self.priority:
                    warnings.warn(
                        message=f"Actor {self.label} has a lower priority than its waiting event {after.label}."
                    )
            elif isinstance(after, list):
                self._after = after
                for actor in after:
                    actor.followers.append(self)
                    if actor.priority > self.priority:
                        warnings.warn(
                            message=f"Actor {self.label} has a lower priority than its waiting event {actor.label}."
                        )
            else:
                raise TypeError(
                    f"Actor {self.label} has a wrong type of waiting event."
                )

        # initialize the time
        if callable(at):
            self._time = round(at(), Mundus.accuracy)
        else:
            self._time = round(at, Mundus.accuracy)

        if callable(step):
            self._step = step
        elif step is not None:
            if step < ((1 / pow(10, Mundus.accuracy)) / 2):
                raise ValueError(
                    f"Current accuracy is {Mundus.accuracy}, step size cannot be smaller than {(1/pow(10, Mundus.accuracy))/2}."
                )
            self._step = round(step, Mundus.accuracy)
        else:
            self._step = step

        if callable(till):
            self._till = till
        elif till is not None:
            self._till = round(till, Mundus.accuracy)
        else:
            self._till = till

        # initialize the status
        self._status = list()
        if active and after is None:
            self.status.append("active")
        else:
            self.status.append("inactive")
        if after is not None:
            self.status.append("onhold")

        # schedule the actor onto timeline
        if self.onhold is False and self.active is True:
            self.timeline.schedule(self)

    def perform(self):
        """Perform the action of this actor. If the actor is continuous, it will return a generator. If the actor is non-continuous, it will return None. Should not be called manually."""
        # non-continuous actor
        if self.active and self.onhold is False:
            if self.step is None and self.till is None:
                self.action(**self.kwargs)
                self.status.append("completed")
                self.status.append("terminated")
                for actor in self.followers:
                    if actor.onhold:
                        actor.activate(force=False)
            # continuous actor but misses step size
            elif self.step is None and self.till is not None:
                raise AttributeError(f"Actor {self.label} has no step size defined.")
            # continuous actor with step size but no end time
            elif self.step is not None and self.till is None:
                while True:
                    self.action(**self.kwargs)
                    if callable(self.step):
                        self._time += round(self.step(), Mundus.accuracy)
                    else:
                        self._time += round(self.step, Mundus.accuracy)
                    yield self.timeline.schedule(self)
            # continuous actor with step size and end time
            elif self.step is not None and self.till is not None:
                if callable(self.till):
                    _till = round(self.till(), Mundus.accuracy)
                    while True:
                        self.action(**self.kwargs)
                        if callable(self.step):
                            self._time += round(self.step(), Mundus.accuracy)
                        else:
                            self._time += round(self.step, Mundus.accuracy)
                        if self.time <= _till:  # type: ignore
                            yield self.timeline.schedule(self)
                        else:
                            self.status.append("completed")
                            self.status.append("terminated")
                            for actor in self.followers:
                                if actor.onhold:
                                    actor.activate(force=False)
                            break
                else:
                    while True:
                        self.action(**self.kwargs)
                        if callable(self.step):
                            self._time += round(self.step(), Mundus.accuracy)
                        else:
                            self._time += round(self.step, Mundus.accuracy)
                        if self.time <= self.till:  # type: ignore
                            yield self.timeline.schedule(self)
                        else:
                            # if this is the last step, activate all followers
                            if self.time >= self.till:
                                self.status.append("completed")
                                self.status.append("terminated")
                                for actor in self.followers:
                                    if actor.onhold:
                                        actor.activate(force=False)
                            break

    def deactivate(self, terminate: bool = True):
        """Deactivate the actor. If terminate is True, the actor will be terminated. If terminate is False, the actor will be put on hold.

        Args:
            terminate (bool, optional): if the actor should be terminated. Defaults to True.
        """
        # if the actor is already inactive, do nothing
        if self.inactive:
            return
        else:
            # deactivate the actor
            self.status.remove("active")
            self.status.append("inactive")
            if terminate:
                self.status.append("terminated")
            else:
                if self.time == self.till:
                    self.status.append("completed")
                    self.status.append("terminated")
                else:
                    self.status.append("onhold")

            # activate all followers
            for actor in self.followers:
                if actor.onhold:
                    actor.activate(force=False)

            # remove all events associated with this actor
            for event in self.timeline.events[:]:
                if event.actor.id == self.id:
                    self.timeline.events.remove(event)

    def activate(self, force: bool = True):
        """Activate the actor. If force is True, the actor will be activated regardless of the waiting targets. If force is False, the actor will be activated only if all waiting targets are completed.

        Args:
            force (bool, optional): if the actor should be forced to be activated. Defaults to True.
        """
        # if the actor is already active, do nothing
        if self.terminated:
            warnings.warn(
                message=f"Actor {self.label} is terminated and cannot be activated."
            )
            return
        elif self.active:
            return
        else:
            # activate the actor if force is True
            if force:
                self.status.remove("inactive")
                if self.onhold:
                    self.status.remove("onhold")
                self.status.append("active")
                self._time = round(self.timeline.now, Mundus.accuracy)
                self.timeline.schedule(self)
            else:
                # activate the actor if all waiting targets are completed
                if all([x.terminated for x in self.after]) is True:
                    self.status.remove("inactive")
                    if self.onhold:
                        self.status.remove("onhold")
                    self.status.append("active")
                    self.timeline.schedule(self)

    def request(self, resource: Resource, amount: Union[int, float] = 1) -> bool:
        """Request a resource from the resource pool. If the resource is available, the actor will perform the action. If the resource is not available, a exception will be throwed.

        Args:
            resource (Resource): the resource.
            amount (Union[int, float], optional): the amount to request. Defaults to 1.

        Returns:
            bool: return True if the request is successful.
        """
        return resource.distribute(self, amount)

    def release(self, resource: Resource, amount: Optional[int | float] = None) -> bool:
        """Release a resource to the resource pool. If the amount is not specified, the actor will release all the resources it has.

        Args:
            resource (Resource): the resource.
            amount (Optional[int  |  float], optional): the amount to be released. Defaults to None.

        Returns:
            bool: return True if the release is successful.
        """
        if amount is None:
            return resource.release(self)
        else:
            return resource.release(self, amount)

    def consume(self, producer: Producer, amount: int = 1):
        """Consume a product from the producer. If the product is available, the actor will perform the action. If the product is not available, a exception will be throwed.

        Args:
            producer (Producer): the producer.
            amount (int, optional): the amount to consume. Defaults to 1.
        """
        return producer.distribute(self, amount)

    @property
    def id(self):
        """The id of the actor."""
        return self._id

    @property
    def label(self):
        """The label of the actor."""
        return self._label

    @property
    def priority(self):
        """The priority of the actor."""
        return self._priority

    @property
    def action(self) -> Callable:
        """The action of the actor."""
        if self._action is not None:
            return self._action
        else:
            raise AttributeError(f"Actor {self.label} has no action defined.")

    @property
    def timeline(self):
        """The timeline of the actor."""
        return self._timeline

    @property
    def time(self):
        """the current time of the actor."""
        return round(self._time, Mundus.accuracy)

    @property
    def till(self):
        """the end time of the actor."""
        return self._till

    @property
    def step(self):
        """the step of the actor."""
        return self._step

    @property
    def status(self):
        """the status of the actor."""
        return self._status

    @property
    def after(self):
        """the actors that must be completed before this actor can be activated."""
        return self._after

    @property
    def active(self):
        """if the actor is active."""
        return "active" in self.status

    @property
    def inactive(self):
        """if the actor is inactive."""
        return "inactive" in self.status

    @property
    def onhold(self):
        """if the actor is on hold."""
        return "onhold" in self.status

    @property
    def scheduled(self):
        """if the actor is scheduled."""
        return "scheduled" in self.status

    @property
    def completed(self):
        """if the actor is completed."""
        return "completed" in self.status

    @property
    def terminated(self):
        """if the actor is terminated."""
        return "terminated" in self.status

    @property
    def followers(self):
        """the actors that will be activated when this actor is completed."""
        return self._followers

    @property
    def kwargs(self):
        """the kwargs of the actor's action function."""
        return self._kwargs


def event(
    at: Union[int, float, Callable] = 0,
    step: Optional[int | float | Callable] = None,
    till: Optional[int | float | Callable] = None,
    after: Optional[List[Actor] | Actor] = None,
    priority: int = 0,
    active: bool = True,
    label: Optional[str] = None,
    on_call: bool = False,
):
    """A decorator to create an event directly from a function.

    Args:
        at (Union[int, float, Callable], optional): when the event should occur, if both step and till are none, then the event only happens once. Defaults to 0.
        step (Optional[int  |  float  |  Callable], optional): how frequently the event should occur, till must also be given. Defaults to None.
        till (Optional[int  |  float  |  Callable], optional): when the event should end, step must also be given. Defaults to None.
        after (Optional[List[Actor]  |  Actor], optional): the event(s) that must happens before this event. Defaults to None.
        priority (int, optional): the priority of the event, if multiple event should happen at the same time, then the event with lower value as priority happens first. Defaults to 0.
        active (bool, optional): whether the event should be active upon creation. Defaults to True.
        label (Optional[str], optional): the short description of this event. Defaults to None.
        on_call (bool, optional): if ture, the event will not be created until the decorated function is called. If false, the event will be create directly without need for calling the decorated function. Defaults to False.
    """    
    def create_event(func):
        def _event(*args, **kwargs):
            # class Event(Actor):
            #     def __init__(
            #         self,
            #         at: Union[int, float, Callable] = 0,
            #         step: Optional[int | float | Callable] = None,
            #         till: Optional[int | float | Callable] = None,
            #         after: Optional[Actor | List[Actor]] = None,
            #         priority: int = 0,
            #         active: bool = True,
            #         label: Optional[str] = None,
            #     ) -> None:
            #         super().__init__(
            #             at=at,
            #             step=step,
            #             till=till,
            #             after=after,
            #             priority=priority,
            #             active=active,
            #             label=label,
            #         )

            #     def action(self):
            #         func(*args, **kwargs)

            actor = Actor(
                action=func,
                at=at,
                step=step,
                till=till,
                after=after,
                priority=priority,
                active=active,
                label=label,
                **kwargs,
            )

            return actor
        if on_call:
            return _event
        else:
            return _event()

    return create_event

