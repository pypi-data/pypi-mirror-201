from __future__ import annotations
from typing import List, Optional, Type, Union, Callable
from uuid import uuid4

from .actor import Actor


class ProductClaim:
    """Record of products claimed by a user."""

    _user: Union[Actor, object]
    _products: List

    def __init__(self, user: Union[Actor, object]) -> None:
        self._user = user
        self._products = list()

    def __eq__(self, __o: ProductClaim) -> bool:
        if self.user is __o.user:
            return True
        else:
            return False

    @property
    def user(self) -> Union[Actor, object]:
        return self._user

    @property
    def quantity(self) -> int:
        return len(self._products)

    @property
    def products(self) -> List:
        return self._products


class Producer:
    """A producer that produces products at a given rate and period."""

    _id: int
    _label: Optional[str]
    _product: Type
    _product_kargs: dict
    _inventory: List
    _capacity: Optional[int]
    _claims: List[ProductClaim]
    _production_period: Union[int, float, Callable]
    _production_rate: int
    _at: Union[int, float, Callable]
    _till: Optional[Union[int, float, Callable]]
    _priority: int

    def __init__(
        self,
        product: Type,
        production_period: Union[int, float, Callable],
        production_rate: int,
        priority: int = 1,
        capacity: Optional[int] = None,
        label: Optional[str] = None,
        at: Union[int, float, Callable] = 0,
        till: Optional[Union[int, float, Callable]] = None,
        **product_kargs,
    ) -> None:
        """Create a producer which produces products at a given rate and period.

        Args:
            product (Type): the product to be produced.
            production_period (Union[int, float]): the cycle period of production.
            production_rate (int): the amount of products to be produced in each cycle.
            priority (int, optional): the production event priority. Defaults to 1.
            capacity (Optional[int], optional): the inventory's capacity. If none, then the capacity is infinite. Defaults to None.
            label (Optional[str], optional): Label of the producer. Defaults to None.
            at (Union[int, float, Callable], optional): when the production starts. Defaults to 0.
            till (Optional[Union[int, float, Callable]], optional): when the production ends. If none, the production never ends. Defaults to None.
        """
        self._id = uuid4().int
        self._label = label or str()
        self._product = product
        self._product_kargs = product_kargs
        self._inventory = list()
        self._production_period = production_period
        self._production_rate = round(production_rate)
        self._capacity = capacity
        self._at = at
        self._till = till
        self._claims = list()

        Actor(
            at=self.at,
            step=self.production_period,
            till=self.till,
            action=self.produce,
            priority=priority,
        )

    def produce(self):
        for _ in range(self.production_rate):
            if self.capacity is None:
                self.inventory.append(self.product(**self.product_kargs))
            else:
                if len(self.inventory) < self.capacity:
                    self.inventory.append(self.product(**self.product_kargs))

    def get(self, quantity: int) -> List:
        """Get products from the inventory."""
        if quantity > len(self.inventory):
            raise ValueError(
                f"Producer {self.label} does not have enough products in inventory."
            )

        products = list()
        for _ in range(quantity):
            products.append(self.inventory.pop())

        return products

    def distribute(self, user: Union[Actor, object], quantity: int):
        """Distribute products to a user."""
        if quantity > len(self.inventory):
            raise ValueError(
                f"Producer {self.label} does not have enough products in inventory."
            )

        for claim in self.claims:
            if claim.user is user:
                claimed_products = list()
                for _ in range(quantity):
                    product = self.inventory.pop()
                    claim.products.append(product)
                    claimed_products.append(product)
                return claimed_products

        claim = ProductClaim(user)
        claimed_products = list()
        for _ in range(quantity):
            product = self.inventory.pop()
            claim.products.append(product)
            claimed_products.append(product)
        self.claims.append(claim)
        return claimed_products

    @property
    def id(self) -> int:
        """Get the producer's id."""
        return self._id

    @property
    def label(self) -> Optional[str]:
        """Get the producer's label."""
        return self._label

    @property
    def product(self) -> Type:
        """Get the product produced by the producer."""
        return self._product

    @property
    def product_kargs(self) -> dict:
        """Get the product's kargs."""
        return self._product_kargs

    @property
    def inventory(self) -> List:
        """Get the producer's inventory."""
        return self._inventory

    @property
    def capacity(self) -> Optional[int]:
        """Get the producer's inventory capacity."""
        return self._capacity

    @property
    def claims(self) -> List[ProductClaim]:
        """Get the producer's claims."""
        return self._claims

    @property
    def production_period(self) -> Union[int, float, Callable]:
        """Get the producer's production period, aka how often the producer produces products. Could be a function."""
        return self._production_period

    @property
    def production_rate(self) -> int:
        """Get the producer's production rate, aka how many products the producer produces in each cycle."""
        return self._production_rate

    @property
    def at(self) -> Union[int, float, Callable]:
        """Get the producer's start time."""
        return self._at

    @property
    def till(self) -> Union[int, float, Callable, None]:
        """Get the producer's end time."""
        return self._till

    @property
    def num_available_products(self) -> int:
        """Get the number of available products in the inventory."""
        return len(self.inventory)
