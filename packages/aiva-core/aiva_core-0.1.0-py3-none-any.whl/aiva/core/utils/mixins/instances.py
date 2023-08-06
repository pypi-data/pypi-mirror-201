# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Generic, Iterator, TypeVar

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from aiva.core.types import Kwargs


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ INSTANCES
# └─────────────────────────────────────────────────────────────────────────────────────

# Declare a TypeVar to represent the instance class
T = TypeVar("T")


class Instances(Generic[T]):
    """A utility class to represent a collection of Python object instances"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of instances by ID
    _instances_by_id: dict[int, T]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self) -> None:
        """Init Method"""

        # Initialize classes by ID
        self._instances_by_id = {}

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ITER__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __iter__(self) -> Iterator[T]:
        """Iter Method"""

        # Iterate over instances
        for instance in self._instances_by_id.values():
            # Yield instance
            yield instance

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ADD
    # └─────────────────────────────────────────────────────────────────────────────────

    def add(self, instance: T | Instances[T]) -> None:
        """Adds an instance to the collection"""

        # Get instances
        instances = instance if isinstance(instance, Instances) else [instance]

        # Iterate over instances
        for instance in instances:
            # Add instance to collection
            self._instances_by_id[id(instance)] = instance

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ UPDATE
    # └─────────────────────────────────────────────────────────────────────────────────

    def update(self, **kwargs: Kwargs) -> None:
        """Updates arbitrary attributes of the current instance"""

        # Update instance attributes
        self.__dict__.update(kwargs)
