# pyright: strict
from copy import deepcopy
from enum import auto
from common_types import Coord, Crop, CropType, Grid, SeedPacketMode, UserInput, WateringCan


class Turnip:
    def __init__(self):
        self._is_watered = False
        self._progress = 0
        self._water_history: list[bool] = []
    @property
    def cost(self) -> int:
        return 300
    @property
    def days_to_grow(self) -> int:
        return 2
    @property
    def is_harvestable(self) -> int:
        return self._progress == self.days_to_grow
    @property
    def value(self) -> int:
        return 500
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
        return "t"
    @property
    def harvest_sprite(self) -> str:
        return "T"
        
class Sunflower:
    def __init__(self):
        self._is_watered = False
        self._progress = 0
        self._water_history: list[bool] = []
    @property
    def cost(self) -> int:
        return 25
    @property
    def days_to_grow(self) -> int:
        return 1
    @property
    def is_harvestable(self) -> int:
        return self._progress == self.days_to_grow
    @property
    def value(self) -> int:
        return 50
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
        return "s"
    @property
    def harvest_sprite(self) -> str:
        return "S"


class Marigold:
    def __init__(self):
        self._is_watered = False
        self._progress = 0
        self._water_history: list[bool] = []
    @property
    def cost(self) -> int:
        return 50
    @property
    def days_to_grow(self) -> int:
        return 2
    @property
    def is_harvestable(self) -> int:
        return self._progress == self.days_to_grow
    @property
    def value(self) -> int:
        return 150
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
        return "m"
    @property
    def harvest_sprite(self) -> str:
        return "M"


class ACCropType(CropType):
    TURNIP = auto()

class PVZCropType(CropType):
    SUNFLOWER = auto()
    MARIGOLD = auto()

class ACMode:
    @property
    def starting_pesos(self) -> int:
        return 1000
    @property
    def grid_size(self) -> tuple[int, int]:
        return 5, 5
    def get_crops(self) -> tuple[CropType, ...]:
        return tuple(e for e in ACCropType)
    def get_crop_instance(self, name: UserInput) -> Crop:
        match ACCropType(name):
            case ACCropType.TURNIP:
                return Turnip()
            
class PVZMode:
    @property
    def starting_pesos(self) -> int:
        return 100
    @property
    def grid_size(self) -> tuple[int, int]:
        return 5, 9
    def get_crops(self) -> tuple[CropType, ...]:
        return tuple(e for e in PVZCropType)
    def get_crop_instance(self, name: UserInput) -> Crop:
        match PVZCropType(name):
            case PVZCropType.SUNFLOWER:
                return Sunflower()
            case PVZCropType.MARIGOLD:
                return Marigold()


class BasicCan:
    def get_watered_cells(self, target: Coord, grid: Grid) -> tuple[Coord, ...]:
        return (target,)
    
class SteelCan:
    def get_watered_cells(self, target: Coord, grid: Grid) -> tuple[Coord, ...]:
        res: list[Coord] = []

        m, n = len(grid), len(grid[0])
        i, j = target
        for ri in range(i-1, i+2): 
            for rj in range(j-1, j+2):
                if 0 <= ri < m and 0 <= rj < n:
                    res.append((ri, rj))
        return tuple(res)
    

class Model:
    def __init__(self, mode: SeedPacketMode, water: WateringCan):
        self._mode = mode
        self._water = water
        self._day = 1
        self._pesos = mode.starting_pesos
        m, n = mode.grid_size
        self._grid: Grid = [[None]*n for _ in range(m)]

    def get_crops(self) -> tuple[CropType, ...]:
        return self._mode.get_crops()
    
    def get_grid(self) -> Grid:
        return deepcopy(self._grid)
    
    def plant_on(self, crop: UserInput, coord: Coord) -> bool:
        if not self._in_bounds(coord):
            return False

        i, j = coord
        if self._grid[i][j] is not None:
            return False
        to_plant = self._mode.get_crop_instance(crop)

        if self._pesos < to_plant.cost:
            return False
        
        self._grid[i][j] = to_plant
        self._pesos -= to_plant.cost
        return True 

    def water_on(self, coord: Coord) -> bool:
        if not self._in_bounds(coord):
            return False
        
        to_water = self._water.get_watered_cells(coord, self._grid)
        for wi, wj in to_water:
            cell = self._grid[wi][wj]
            match cell:
                case None:
                    continue
                case _:
                    cell.water()
        return True

    def harvest_all(self) -> bool:
        harvested = False
        n, m = len(self._grid), len(self._grid[0])
        for i in range(n):
            for j in range(m):
                cell = self._grid[i][j]
                match cell:
                    case None:
                        continue
                    case _:
                        if cell.is_harvestable:
                            harvested = True
                            self._pesos += cell.value
                            self._grid[i][j] = None
        return harvested

    def get_pesos(self):
        return self._pesos
    
    def get_day(self):
        return self._day

    def next_day(self):
        self._day += 1
        n, m = len(self._grid), len(self._grid[0])
        for i in range(n):
            for j in range(m):
                cell = self._grid[i][j]
                match cell:
                    case None:
                        continue
                    case _:
                        cell.update()

    def _in_bounds(self, coord: Coord):
        i, j = coord
        m, n = len(self._grid), len(self._grid[0])
        return 0 <= i < m and 0 <= j < n 

