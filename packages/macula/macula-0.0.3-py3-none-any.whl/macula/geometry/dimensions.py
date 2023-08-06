import json

import numpy as np


class Dimensions:
    def __init__(self, width: int, height: int, depth: int, profile: int, passe_partout: int):
        self.depth = depth
        self.profile = profile
        self.passe_partout = passe_partout
        self.picture = Surface(
            width=width,
            height=height,
            origin=(0, 0),
        )
        self.inner = Surface(
            width=self.picture.width + (2 * passe_partout),
            height=self.picture.height + (2 * passe_partout),
            origin=(0, 0),
        )
        self.frame = Surface(
            width=self.inner.width + (2 * profile),
            height=self.inner.height + (2 * profile),
            origin=(0, 0),
        )
        # corners
        self.corners = [Surface(
            width=profile,
            height=profile,
            origin=origin,
        ) for origin in [
            (-self.inner.width / 2 - profile / 2, self.inner.height / 2 + profile / 2),  # top left
            (self.inner.width / 2 + profile / 2, self.inner.height / 2 + profile / 2),  # top right
            (-self.inner.width / 2 - profile / 2, -self.inner.height / 2 - profile / 2),  # bottom left
            (self.inner.width / 2 + profile / 2, -self.inner.height / 2 - profile / 2)  # bottom right
        ]]
        # x sides
        self.x_sides = [Surface(
            width=self.inner.width,
            height=profile,
            origin=origin,
        ) for origin in [
            (-self.inner.width / 2 - profile / 2, 0),  # left
            (self.inner.width / 2 + profile / 2, 0)  # right
        ]]
        # y sides
        self.y_sides = [Surface(
            width=profile,
            height=self.inner.height,
            origin=origin,
        ) for origin in [
            (0, self.inner.height / 2 + profile / 2),  # top
            (0, -self.inner.height / 2 - profile / 2)  # bottom
        ]]

    def to_json(self, path: str):
        with open(path, "w") as file:
            json.dump({
                "unit": "mm",
                "picture": {
                    "width": self.picture.width,
                    "height": self.picture.height,
                    "origin": self.picture.origin
                },
                "inner": {
                    "width": self.inner.width,
                    "height": self.inner.height,
                    "origin": self.inner.origin
                },
                "frame": {
                    "width": self.frame.width,
                    "height": self.frame.height,
                    "depth": self.depth,
                    "origin": self.frame.origin
                },
                "corners": {
                    "top_left": {
                        "width": self.corners[0].width,
                        "height": self.corners[0].height,
                        "origin": self.corners[0].origin,
                        "direction": {
                            "start": self.corners[0].start,
                            "stop": self.corners[0].stop,
                        }
                    },
                    "top_right": {
                        "width": self.corners[1].width,
                        "height": self.corners[1].height,
                        "origin": self.corners[1].origin,
                        "direction": {
                            "start": self.corners[1].start,
                            "stop": self.corners[1].stop,
                        }
                    },
                    "bottom_left": {
                        "width": self.corners[2].width,
                        "height": self.corners[2].height,
                        "origin": self.corners[2].origin,
                        "direction": {
                            "start": self.corners[2].start,
                            "stop": self.corners[2].stop,
                        }
                    },
                    "bottom_right": {
                        "width": self.corners[3].width,
                        "height": self.corners[3].height,
                        "origin": self.corners[3].origin,
                        "direction": {
                            "start": self.corners[3].start,
                            "stop": self.corners[3].stop,
                        }
                    }
                },
                "x_sides": {
                    "left": {
                        "width": self.x_sides[0].width,
                        "height": self.x_sides[0].height,
                        "origin": self.x_sides[0].origin,
                        "direction": {
                            "start": self.x_sides[0].start,
                            "stop": self.x_sides[0].stop,
                        }
                    },
                    "right": {
                        "width": self.x_sides[1].width,
                        "height": self.x_sides[1].height,
                        "origin": self.x_sides[1].origin,
                        "direction": {
                            "start": self.x_sides[1].start,
                            "stop": self.x_sides[1].stop,
                        }
                    }
                },
                "y_sides": {
                    "top": {
                        "width": self.y_sides[0].width,
                        "height": self.y_sides[0].height,
                        "origin": self.y_sides[0].origin,
                        "direction": {
                            "start": self.y_sides[0].start,
                            "stop": self.y_sides[0].stop,
                        }
                    },
                    "bottom": {
                        "width": self.y_sides[1].width,
                        "height": self.y_sides[1].height,
                        "origin": self.y_sides[1].origin,
                        "direction": {
                            "start": self.y_sides[1].start,
                            "stop": self.y_sides[1].stop,
                        }
                    }
                }
            }, file, indent=4)

    def from_json(self, path: str):
        with open(path, "w") as file:
            contents = file.read()

        parsed_json = json.loads(contents)
        return parsed_json


class Surface:
    def __init__(self, width: int, height: int, origin: tuple):
        self.width = width
        self.height = height
        self.origin = origin

        self.start, self.stop = self.calculate_direction()
        self.inner_polyon = self.calculate_inner()
        self.middle_polygon = self.calculate_middle()
        self.outer_polygon = self.calculate_outer()

    def calculate_direction(self):
        print("Calculating direction")
        width = self.width
        height = self.height

        if width == height:
            start = (width, height)
            stop = (0, 0)
            return [start, stop]
        elif width > height:
            start = (int(width / 2), height)
            stop = (int(width / 2), 0)
            return [start, stop]
        else:
            start = (width, int(height / 2))
            stop = (0, int(height / 2))
            return [start, stop]

    def calculate_inner(self) -> np.ndarray:
        width = self.width
        height = self.height

        if width == height:
            polygon = np.array([
                [int(width / 3 * 2), int(height / 3 * 2)],
                [width, int(height / 3 * 2)],
                [width, height],
                [int(width / 3 * 2), height]
            ])
        elif width > height:
            polygon = np.array([
                [0, int(height / 3 * 2)],
                [width, int(height / 3 * 2)],
                [width, height],
                [0, height]
            ])
        else:
            polygon = np.array([
                [int(width / 3 * 2), 0],
                [width, 0],
                [width, height],
                [int(width / 3 * 2), height]
            ])
        return polygon

    def calculate_middle(self) -> np.ndarray:
        width = self.width
        height = self.height

        if width == height:
            polygon = np.array([
                [int(width / 3), int(height / 3)],
                [width, int(height / 3)],
                [width, int(height / 3 * 2)],
                [int(width / 3 * 2), int(height / 3 * 2)],
                [int(width / 3 * 2), height],
                [int(width / 3), height]
            ])
        elif width > height:
            polygon = np.array([
                [0, int(height / 3)],
                [width, int(height / 3)],
                [width, int(height / 3 * 2)],
                [0, int(height / 3 * 2)],
            ])
        else:
            polygon = np.array([
                [int(width / 3), 0],
                [int(width / 3 * 2), 0],
                [int(width / 3 * 2), height],
                [int(width / 3), height],
            ])
        return polygon

    def calculate_outer(self) -> np.ndarray:
        width = self.width
        height = self.height

        if width == height:
            polygon = np.array([
                [0, 0],
                [width, 0],
                [width, int(height / 3)],
                [int(width / 3), int(height / 3)],
                [int(width / 3), height],
                [0, height]
            ])
        elif width > height:
            polygon = np.array([
                [0, 0],
                [width, 0],
                [width, int(height / 3)],
                [0, int(height / 3)],
            ])
        else:
            polygon = np.array([
                [0, 0],
                [int(width / 3), 0],
                [int(width / 3), height],
                [0, height]
            ])
        return polygon
