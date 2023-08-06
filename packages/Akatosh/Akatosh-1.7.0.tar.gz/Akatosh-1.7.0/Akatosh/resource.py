from __future__ import annotations
from typing import Union, List, Optional, TYPE_CHECKING
from dataclasses import dataclass
from uuid import uuid4

from .universe import Mundus

if TYPE_CHECKING:
    from .actor import Actor


@dataclass
class ResourceClaim:
    """Resource claim record of a user. Each user only have one resource claim for a resource."""

    _user: Union[Actor, object]
    _quantity: Union[int, float]

    def __eq__(self, __o: ResourceClaim) -> bool:
        if self.user is __o.user:
            return True
        else:
            return False

    @property
    def user(self) -> Union[Actor, object]:
        return self._user

    @property
    def quantity(self) -> Union[int, float]:
        return self._quantity


@dataclass
class ResourceUsageRecord:
    """Resource usage record."""

    _at: Union[int, float]
    _quantity: Union[int, float]

    def __eq__(self, __o: ResourceUsageRecord) -> bool:
        if self.at == __o.at and self.quantity == __o.quantity:
            return True
        else:
            return False
        
    def __str__(self) -> str:
        return f"{self.at}:{self.quantity}"

    @property
    def at(self) -> Union[int, float]:
        return self._at

    @property
    def quantity(self) -> Union[int, float]:
        return self._quantity


class Resource:
    _id: int
    _label: str
    _capacity: Union[int, float]
    _claimed_quantity: Union[int, float]

    _claims: List[ResourceClaim]
    _records: List[ResourceUsageRecord]

    def __init__(
        self,
        label: Optional[str] = None,
        capacity: Union[int, float] = 1,
        init_claimed_quantity: Union[int, float] = 0,
    ) -> None:
        """Create a resource object. The resource can be claimed by users, or distribute to users. The resource can be released from users. The resource can be put back or get from the resource pool anonymously.

        Args:
            label (Optional[str], optional): the label of the resources. Defaults to None.
            capacity (Union[int, float], optional): _description_. the capacity of the resource to 1.
            init_claimed_quantity (Union[int, float], optional): the initial amount of resource in use. Defaults to 0.
        """
        self._id = uuid4().int
        self._label = label or str()
        self._capacity = capacity
        self._claimed_quantity = init_claimed_quantity

        self._claims = list()
        self._records = list()

    def get(self, quantity: Union[int, float]) -> bool:
        """Anonymous user get resource from resource pool. No resource claim is created."""
        if quantity <= self.available_quantity:
            self._claimed_quantity += quantity
            self.records.append(ResourceUsageRecord(Mundus.now, self.claimed_quantity))
            return True
        else:
            raise ValueError(
                f"Quantity {quantity} is greater than available quantity {self.available_quantity} of resource {self.label}."
            )

    def put(self, quantity: Union[int, float]) -> bool:
        """Anonymous user put resource back to resource pool. No resource claim is checked."""
        if quantity <= self.claimed_quantity:
            self._claimed_quantity -= quantity
            self.records.append(ResourceUsageRecord(Mundus.now, self.claimed_quantity))
            return True
        else:
            raise ValueError(
                f"Quantity {quantity} is greater than claimed quantity {self.claimed_quantity} of resource {self.label}."
            )

    def distribute(
        self, user: Union[Actor, object], quantity: Union[int, float]
    ) -> bool:
        """Distribute a amount of resource to a user. If the user already has a claim, the quantity will be added to the claim. Otherwise, a new claim will be created.

        Args:
            user (Union[Actor, object]): the user to distribute resource to.
            quantity (Union[int, float]): the amount of resource to distribute.

        Raises:
            ValueError: if the quantity is greater than available quantity.

        Returns:
            bool: return True if the distribution is successful.
        """
        if quantity <= self.available_quantity:
            self._claimed_quantity += quantity
            for claim in self.claims:
                if claim.user is user:
                    claim._quantity += quantity
                    return True
            resource_claim = ResourceClaim(user, quantity)
            self.claims.append(resource_claim)
            self.records.append(ResourceUsageRecord(Mundus.now, self.claimed_quantity))
            return True
        else:
            raise ValueError(
                f"Quantity {quantity} is greater than available quantity {self.available_quantity} of resource {self.label}."
            )

    def release(
        self,
        user: Optional[Actor | List[Actor] | object | List[object]] = None,
        amount: Optional[int | float] = None,
    ) -> bool:
        """Release resource from a user or group of users. If the user is no longer using any resource, the resource claim will be removed. if no user is specified, all resource claims will be removed.
        Args:
            user (Optional[Actor  |  List[Actor]  |  object  |  List[object]], optional): the user or group of users. Defaults to None.
            amount (Optional[int  |  float], optional): the amount of resource to release. Defaults to None.

        Raises:
            ValueError: raised if the amount is greater than the user claimed quantity.

        Returns:
            bool: return True if the release is successful.
        """
        if user is None:
            self._claimed_quantity = 0
            self._claims.clear()
            return True
        else:
            if isinstance(user, list):
                for u in user:
                    for claim in self.claims[:]:
                        if claim.user is u:
                            if amount is None:
                                if claim.quantity > self.claimed_quantity:
                                    raise ValueError(
                                        f"Resource claim's quantity {claim.quantity} is greater than claimed quantity {self.claimed_quantity} of resource {self.label}."
                                    )
                                else:
                                    self._claimed_quantity -= claim.quantity
                                    self.claims.remove(claim)
                            else:
                                if amount > claim.quantity:
                                    raise ValueError(
                                        f"User tries to release {amount} units, but only {claim.quantity} units are claimed by the user from resource {self.label}."
                                    )
                                else:
                                    self._claimed_quantity -= amount
                                    claim._quantity -= amount
                                    if claim.quantity == 0:
                                        self.claims.remove(claim)
            else:
                for claim in self.claims[:]:
                    if claim.user is user:
                        if amount is None:
                            if claim.quantity > self.claimed_quantity:
                                raise ValueError(
                                    f"Resource claim's quantity {claim.quantity} is greater than claimed quantity {self.claimed_quantity} of resource {self.label}."
                                )
                            else:
                                self._claimed_quantity -= claim.quantity
                                self.claims.remove(claim)
                        else:
                            if amount > claim.quantity:
                                raise ValueError(
                                    f"User tries to release {amount} units, but only {claim.quantity} units are claimed by the user from resource {self.label}."
                                )
                            else:
                                self._claimed_quantity -= amount
                                claim._quantity -= amount
                                if claim.quantity == 0:
                                    self.claims.remove(claim)
            self.records.append(ResourceUsageRecord(Mundus.now, self.claimed_quantity))
            return True

    @property
    def id(self) -> int:
        """The id of the resource."""
        return self._id

    @property
    def label(self) -> str:
        """The label of the resource."""
        return self._label

    @property
    def capacity(self) -> Union[int, float]:
        """The capacity of the resource."""
        return self._capacity

    @property
    def claimed_quantity(self) -> Union[int, float]:
        """The amount of resource claimed by users."""
        return self._claimed_quantity

    @property
    def available_quantity(self) -> Union[int, float]:
        """The amount of resource available for distribution."""
        return self.capacity - self.claimed_quantity

    @property
    def claims(self) -> List[ResourceClaim]:
        """The list of resource claims."""
        return self._claims

    @property
    def records(self) -> List[ResourceUsageRecord]:
        """The list of resource records."""
        return self._records

    @property
    def users(self):
        """The list of users who have claimed the resource."""
        return [claim.user for claim in self.claims]

    @property
    def utilization(self) -> Union[int, float]:
        """The utilization of the resource."""
        return self.claimed_quantity / self.capacity

    def utilization_in_past(
        self,
        period: Union[int, float],
        at: Optional[Union[int, float]] = None,
    ):
        """Get the resource utilization in the past period.

        Args:
            period (Union[int, float]): the period to look back.
            at (Union[int, float], optional): from when to look back. Defaults to Mundus.now.
        """
        if at is None:
            at = Mundus.now
            usage_records = [
                record
                for record in self.records
                if record.at >= at - period and record.at <= at
            ]
        else:
            usage_records = [
                record
                for record in self.records
                if record.at >= at - period and record.at <= at
            ]

        if len(usage_records) == 0:
            return self.claimed_quantity / self.capacity
        else:
            usage_records.sort(key=lambda x: x.at)
            weighted_average_usage = 0
            for i, record in enumerate(usage_records):
                if i == 0:
                    weighted_average_usage += (
                        record.quantity * (record.at - (at-period)) / period
                    )
                else:
                    weighted_average_usage += (
                        record.quantity * (record.at - usage_records[i - 1].at) / period
                    )
            return weighted_average_usage / self.capacity
