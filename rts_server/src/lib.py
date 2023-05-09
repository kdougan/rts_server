from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field


@dataclass(slots=True)
class GameState:
    players: dict[int, Player] = field(default_factory=dict)


@dataclass(slots=True)
class Player:
    id: int
    name: str
    units: list[Unit] = field(default_factory=list)
    buildings: list[Building] = field(default_factory=list)


@dataclass(slots=True)
class Unit:
    id: int
    type: int
    pos: tuple[int, int]


@dataclass(slots=True)
class Building:
    id: int
    type: int
    pos: tuple[int, int]
    tick_interval: int = 1000
    last_tick: int = 0

    def tick(self, current_time: int) -> bool:
        if current_time - self.last_tick >= self.tick_interval:
            self.last_tick = current_time
            return True
        return False
