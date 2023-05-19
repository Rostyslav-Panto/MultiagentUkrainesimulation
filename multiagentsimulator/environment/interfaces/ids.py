from dataclasses import dataclass


@dataclass(frozen=True)
class LocationID:
    name: str


@dataclass(frozen=True)
class PersonID:
    name: str
    age: int
