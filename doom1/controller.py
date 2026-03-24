from common_types import Command
from model_part1 import Model
from view import View


class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self._model = model
        self._view = view

    def start(self):
        self._view.print_day(self._model.get_day())
        self._view.print_grid(
            self._model.get_pesos(), self._model.get_grid()
            )
            
        while True:
            cmd: Command = self._view.prompt_command()

            match cmd:
                case Command.PLANT:
                    crop = self._view.prompt_crop(self._model.get_crops())
                    if not crop:
                        self._view.print_failed()
                        continue
                    
                    coord = self._view.prompt_coord(self._model.get_grid())
                    if not coord:
                        self._view.print_failed()
                        continue

                    if not self._model.plant_on(crop, coord):
                        self._view.print_failed()
                        continue
                    self._view.print_success()
                    
                case Command.WATER:
                    coord = self._view.prompt_coord(self._model.get_grid())
                    if not coord:
                        self._view.print_failed()
                        continue
      
                    if not self._model.water_on(coord):
                        self._view.print_failed()
                        continue
                    self._view.print_success()

                case Command.HARVEST:
                    if not self._model.harvest_all():
                        self._view.print_failed()
                        self._view.print_new_line()
                        continue
                    self._view.print_success()

                case Command.GRID_STATUS:
                    self._view.print_grid(
                        self._model.get_pesos(), self._model.get_grid()
                        )
                    
                case Command.NEXT_DAY:
                    self._model.next_day()
                    self._view.print_day_ended()
                    self._view.print_new_line()
                    self._view.print_day(self._model.get_day())
                    self._view.print_grid(
                        self._model.get_pesos(), self._model.get_grid()
                        )
