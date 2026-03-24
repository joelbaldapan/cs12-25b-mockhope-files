# pyright: strict
from __future__ import annotations
from enum import StrEnum, auto
from typing import Protocol


type UserInput = str
type Coord = tuple[int, int]
type Grid = list[list[None | Crop]]

class CropType(StrEnum):
    ...

class Command(StrEnum):
    PLANT = auto()
    WATER = auto()
    HARVEST = auto()
    GRID_STATUS = auto()
    NEXT_DAY = auto()

class Crop(Protocol):
    @property
    def cost(self) -> int:
        ...
    @property
    def days_to_grow(self) -> int:
        ...
    @property
    def is_harvestable(self) -> int:
        ...
    @property
    def value(self) -> int:
        ...
    def water(self):
        ...
    def update(self):
        ...
    @property
    def growing_sprite(self) -> str:
        ...
    @property
    def harvest_sprite(self) -> str:
        ...

class SeedPacketMode(Protocol):
    @property
    def starting_pesos(self) -> int:
        ...
    @property
    def grid_size(self) -> tuple[int, int]:
        ...
    def get_crops(self) -> tuple[CropType, ...]:
        ...
    def get_crop_instance(self, name: UserInput) -> Crop:
        ...
    

class WateringCan(Protocol):
    def get_watered_cells(self, target: Coord, grid: Grid) -> tuple[Coord, ...]:
        ...