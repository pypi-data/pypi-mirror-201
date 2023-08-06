import os

from macula.geometry.dimensions import Dimensions
from macula.geometry.dimensions import Surface


class Frame:
    def __init__(self, name: str, dimensions: Dimensions, debug: bool = False):
        print(f"Initiate Frame {name}")
        self.name = name
        self.dimensions = dimensions
        self.debug = debug

    def save(self, dir: str):
        print(f"Saving Frame {self.name}")
        os.makedirs(f"{dir}/{self.name}", exist_ok=True)
        self.dimensions.to_json(path=f"{dir}/{self.name}/dimensions.json")


class Side:
    def __init__(self, name: str, dimensions: Surface):
        self.name = name
        self.dimensions = dimensions


class Corner:
    def __init__(self, name: str, dimensions: Surface):
        self.name = name
        self.dimensions = dimensions
