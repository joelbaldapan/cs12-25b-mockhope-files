# pyright: strict

from argparse import ArgumentParser
from common_types import SeedPacketMode, WateringCan
from model_part1 import ACMode, BasicCan, Model, PVZMode, SteelCan
from model_part2 import KoyukiCan, SDVMode, WaterBucket
from view import View
from controller import Controller

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--mode", type=str, required=True)
    parser.add_argument("--water", type=str, required=True)
    args = parser.parse_args()

    mode: SeedPacketMode = ACMode()
    match args.mode:
        case "ac":
            mode = ACMode()
        case "pvz":
            mode = PVZMode()
        case "sdv":
            mode = SDVMode()
        case _:
            raise ValueError("Invalid seed packet mode.")

    water: WateringCan = BasicCan()
    match args.water:
        case "basic":
            water = BasicCan()
        case "steel":
            water = SteelCan()
        case "koyuki":
            water = KoyukiCan()
        case "bucket":
            water = WaterBucket()
        case _:
            raise ValueError("Invalid watering can.")

    model = Model(mode, water)
    view = View()
    controller = Controller(model, view)
    controller.start()