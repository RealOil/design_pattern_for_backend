from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class User:
    id: int
    name: str


class UserRepository(Protocol):
    def save(self, user: User) -> None: ...
