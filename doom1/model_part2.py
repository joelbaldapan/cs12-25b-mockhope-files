# pyright: strict

from enum import auto
from common_types import Coord, Crop, CropType, Grid, UserInput


class SDVCropType(CropType):
    PARSNIP = auto()
    SWEET_GEM_BERRY = auto()
    ANCIENT_FRUIT = auto()

class Parsnip:
    def __init__(self):
        self._is_watered = False
        self._progress = 0
        self._water_history: list[bool] = []
    @property
    def cost(self) -> int:
        return 100
    @property
    def days_to_grow(self) -> int:
        return 1
    @property
    def is_harvestable(self) -> int:
        return self._progress == self.days_to_grow
    @property
    def value(self) -> int:
        return 200
    def water(self):
        self._is_watered = True
    def update(self):
        if self.is_harvestable:
            return
        if self._is_watered:
            self._progress += 1
        self._water_history.append(self._is_watered)
        self._is_watered = False
    @property
    def growing_sprite(self) -> str:
        return "p"
    @property
    def harvest_sprite(self) -> str:
        return "P"

class SweetGemBerry:
    def __init__(self):
        self._is_watered = False
        self._progress = 0
        self._water_history: list[bool] = []
    @property
    def cost(self) -> int:
        return 300
    @property
    def days_to_grow(self) -> int:
        return 3
    @property
    def is_harvestable(self) -> int:
        return self._progress == self.days_to_grow
    @property
    def value(self) -> int:
        return 1000
    def water(self):
        self._is_watered = True
    def update(self):
        if self.is_harvestable:
            return
        watered_yesterday = (self._water_history[-1] 
                             if self._water_history else False)
        if self._is_watered and watered_yesterday:
            self._progress += 1
        self._water_history.append(self._is_watered)
        self._is_watered = False
    @property
    def growing_sprite(self) -> str:
        return "g"
    @property
    def harvest_sprite(self) -> str:
        return "G"

class AncientFruit:
    def __init__(self):
        self._is_watered = False
        self._progress = 0
        self._water_history: list[bool] = []
    @property
    def cost(self) -> int:
        return 1000
    @property
    def days_to_grow(self) -> int:
        return 14
    @property
    def is_harvestable(self) -> int:
        return self._progress >= self.days_to_grow
    @property
    def value(self) -> int:
        return 6700
    def water(self):
        self._is_watered = True
    def update(self):
        if self.is_harvestable:
            return
        self._water_history.append(self._is_watered)
        if self._is_watered:
            k = 0
            for w in reversed(self._water_history):
                if w:
                    k += 1
                else:
                    break
            self._progress = min(self.days_to_grow, self._progress + k)
        self._is_watered = False
    @property
    def growing_sprite(self) -> str:
        return "a"
    @property
    def harvest_sprite(self) -> str:
        return "A"

class SDVMode:
    @property
    def starting_pesos(self) -> int:
        # return 400
        return 7000
    @property
    def grid_size(self) -> tuple[int, int]:
        return 9, 9
    def get_crops(self) -> tuple[CropType, ...]:
        return tuple(e for e in SDVCropType)
    def get_crop_instance(self, name: UserInput) -> Crop:
        match SDVCropType(name):
            case SDVCropType.PARSNIP:
                return Parsnip()
            case SDVCropType.SWEET_GEM_BERRY:
                return SweetGemBerry()
            case SDVCropType.ANCIENT_FRUIT:
                return AncientFruit()

class KoyukiCan:
    def get_watered_cells(self, target: Coord, grid: Grid) -> tuple[Coord, ...]:
        res: list[Coord] = []
        m, n = len(grid), len(grid[0])
        i, j = target

        for ri in range(m):
            for rj in range(n):
                if abs(ri - i) + abs(rj - j) <= 2:
                    res.append((ri, rj))
                    
        return tuple(res)

class WaterBucket:
    def get_watered_cells(self, target: Coord, grid: Grid) -> tuple[Coord, ...]:
        ti, tj = target
        m, n = len(grid), len(grid[0])
        
        visited: set[Coord] = set()
        res: list[Coord] = []

        def dfs(i: int, j: int):
            if not (0 <= i < m and 0 <= j < n):
                return
            if (i, j) in visited or grid[i][j] is None:
                return

            visited.add((i, j))
            res.append((i, j))
            
            dfs(i+1, j)
            dfs(i-1, j)
            dfs(i, j+1)
            dfs(i, j-1)
            
        dfs(ti, tj)
        return tuple(res)