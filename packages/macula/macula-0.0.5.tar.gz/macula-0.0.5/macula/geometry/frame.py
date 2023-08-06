import json
import os
import uuid

from macula.geometry.primitives import Plane


class Frame:
    def __init__(self):
        self.name = str(uuid.uuid4())
        print(f"Created frame: {self.name}")
        self.orientation = "landscape"
        self.unit = "mm"
        self.depth = 10
        self.picture = Plane(width=100, height=100)
        self.passe_partout = Plane(
            width=self.picture.width + 10,
            height=self.picture.height + 10
        )
        self.profile = Plane(
            width=self.passe_partout.width + 10,
            height=self.passe_partout.height + 10
        )

        self.corners = []
        self.x_sides = []
        self.y_sides = []

    def build(self):
        print(f"Building frame {self.name}")
        profile = self.profile.width - self.passe_partout.width
        inner = self.passe_partout

        top_left = Plane(width=profile, height=profile)
        top_left.set_origin(origin=(-inner.width / 2 - profile / 2, inner.height / 2 + profile / 2))

        top_right = Plane(width=profile, height=profile)
        top_right.set_origin(origin=(inner.width / 2 + profile / 2, inner.height / 2 + profile / 2))

        bottom_left = Plane(width=profile, height=profile)
        bottom_left.set_origin(origin=(-inner.width / 2 - profile / 2, -inner.height / 2 - profile / 2))

        bottom_right = Plane(width=profile, height=profile)
        bottom_right.set_origin(origin=(inner.width / 2 + profile / 2, -inner.height / 2 - profile / 2))

        top_side = Plane(width=inner.width, height=profile)
        top_side.set_origin(origin=(0, inner.height / 2 + profile / 2))

        bottom_side = Plane(width=inner.width, height=profile)
        bottom_side.set_origin(origin=(0, -inner.height / 2 - profile / 2))

        left_side = Plane(width=profile, height=inner.height)
        left_side.set_origin(origin=(-inner.width / 2 - profile / 2, 0))

        right_side = Plane(width=profile, height=inner.height)
        right_side.set_origin(origin=(inner.width / 2 + profile / 2, 0))

        self.corners = [top_left, top_right, bottom_left, bottom_right]
        self.x_sides = [top_side, bottom_side]
        self.y_sides = [left_side, right_side]

    def set_orientation(self, orientation: str):
        self.orientation = orientation

    def set_picture(self, width: int, height: int):
        self.picture = Plane(width=width, height=height)

    def set_passe_partout(self, thickness: int):
        self.passe_partout = Plane(
            width=self.picture.width + thickness,
            height=self.picture.height + thickness
        )

    def set_profile(self, thickness: int):
        self.profile = Plane(
            width=self.passe_partout.width + thickness,
            height=self.passe_partout.height + thickness
        )

    def set_depth(self, depth: int):
        self.depth = depth

    def from_json(self, path: str):
        print(f"Loading dimensions from {path}")
        with open(path, "r") as rf:
            data = json.load(rf)

        picture = data["picture"]
        passe_partout = data["passe_partout"]
        profile = data["profile"]

        top_left = data["corners"]["top_left"]
        top_left_plane = Plane(width=top_left["width"], height=top_left["height"])
        top_left_plane.set_origin(origin=top_left["origin"])

        top_right = data["corners"]["top_right"]
        top_right_plane = Plane(width=top_right["width"], height=top_right["height"])
        top_right_plane.set_origin(origin=top_right["origin"])

        bottom_left = data["corners"]["top_right"]
        bottom_left_plane = Plane(width=bottom_left["width"], height=bottom_left["height"])
        bottom_left_plane.set_origin(origin=bottom_left["origin"])

        bottom_right = data["corners"]["top_right"]
        bottom_right_plane = Plane(width=bottom_right["width"], height=bottom_right["height"])
        bottom_right_plane.set_origin(origin=bottom_right["origin"])

        left = data["x_sides"]["left"]
        left_plane = Plane(width=left["width"], height=left["height"])
        left_plane.set_origin(origin=left["origin"])

        right = data["x_sides"]["right"]
        right_plane = Plane(width=right["width"], height=right["height"])
        right_plane.set_origin(origin=left["origin"])

        top = data["y_sides"]["top"]
        top_plane = Plane(width=top["width"], height=top["height"])
        top_plane.set_origin(origin=left["origin"])

        bottom = data["y_sides"]["bottom"]
        bottom_plane = Plane(width=bottom["width"], height=bottom["height"])
        bottom_plane.set_origin(origin=left["origin"])

        self.unit = "mm"
        self.depth = data["profile"]["depth"]
        self.picture = Plane(width=picture["width"], height=picture["height"])
        self.passe_partout = Plane(width=passe_partout["width"], height=passe_partout["height"])
        self.profile = Plane(width=profile["width"], height=profile["height"])

        self.corners = [top_left_plane, top_left_plane, top_right_plane, bottom_left_plane]
        self.x_sides = [top_plane, bottom_plane]
        self.y_sides = [left_plane, right_plane]

    def to_json(self, dir: str):
        print(f"Saving frame {self.name}")
        os.makedirs(f"{dir}/{self.name}", exist_ok=True)

        self.build()
        with open(f"{dir}/{self.name}/dimensions.json", "w") as file:
            json.dump({
                "unit": self.unit,
                "picture": {
                    "width": self.picture.width,
                    "height": self.picture.height,
                    "origin": self.picture.origin
                },
                "passe_partout": {
                    "width": self.passe_partout.width,
                    "height": self.passe_partout.height,
                    "origin": self.passe_partout.origin
                },
                "profile": {
                    "width": self.profile.width,
                    "height": self.profile.height,
                    "depth": self.depth,
                    "origin": self.profile.origin
                },
                "corners": {
                    "top_left": {
                        "width": self.corners[0].width,
                        "height": self.corners[0].height,
                        "origin": self.corners[0].origin
                    },
                    "top_right": {
                        "width": self.corners[1].width,
                        "height": self.corners[1].height,
                        "origin": self.corners[1].origin
                    },
                    "bottom_left": {
                        "width": self.corners[2].width,
                        "height": self.corners[2].height,
                        "origin": self.corners[2].origin
                    },
                    "bottom_right": {
                        "width": self.corners[3].width,
                        "height": self.corners[3].height,
                        "origin": self.corners[3].origin
                    }
                },
                "x_sides": {
                    "left": {
                        "width": self.x_sides[0].width,
                        "height": self.x_sides[0].height,
                        "origin": self.x_sides[0].origin
                    },
                    "right": {
                        "width": self.x_sides[1].width,
                        "height": self.x_sides[1].height,
                        "origin": self.x_sides[1].origin
                    }
                },
                "y_sides": {
                    "top": {
                        "width": self.y_sides[0].width,
                        "height": self.y_sides[0].height,
                        "origin": self.y_sides[0].origin
                    },
                    "bottom": {
                        "width": self.y_sides[1].width,
                        "height": self.y_sides[1].height,
                        "origin": self.y_sides[1].origin
                    }
                }
            }, file, indent=4)
