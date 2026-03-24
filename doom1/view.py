# pyright: strict
from common_types import Command, Coord, CropType, Grid, UserInput


class View:
    def prompt_command(self) -> Command:
        print("Action:")
        while True:
            inp = input("- ")
            inp = inp.lower()
            match inp:
                case "p":
                    return Command.PLANT 
                case "w":
                    return Command.WATER 
                case "h":
                    return Command.HARVEST 
                case "g":
                    return Command.GRID_STATUS
                case "n":
                    return Command.NEXT_DAY
                case _:
                    continue

    def prompt_crop(self, crops: tuple[CropType, ...]) -> UserInput | None:
        print(f"Crops: ", end="")
        names = tuple(crop.name.lower() for crop in crops)
        for i in range(len(names)):
            if i < len(names)-1:
                print(names[i], end=", ")
            else:
                print(names[i], end="")
        print()

        inp = input("- ")
        for crop in crops:
            if crop.name.lower() == inp.lower():
                return inp.lower()
        return None

    def prompt_coord(self, grid: Grid) -> Coord | None:
        print("Location (i j):")
        raw = input("- ")
        try:
            inp = raw.split()
            if len(inp) != 2:
                return None
            v1, v2 = tuple(map(int, inp))
            return (v1, v2)
        except:
            return None

    def print_day(self, day: int):
        print("=====")
        print()
        print(f"Day {day}")

    def print_grid(self, pesos: int, grid: Grid):
        m, n = len(grid), len(grid[0])
        print(f"Pesos: {pesos}")
        for i in range(m):
            for j in range(n):
                cell = grid[i][j]
                match cell:
                    case None:
                        print(".", end="")
                    case _:
                        if cell.is_harvestable:
                            print(cell.harvest_sprite, end="")
                        else:
                            print(cell.growing_sprite, end="")
                if j != n-1:
                    print(" ", end='')
            print()
        print()

    def print_day_ended(self):
        print('Day ended.')
        print()

    def print_success(self):
        print('Success!')
        print()

    def print_failed(self):
        print('Failed.')
        print()