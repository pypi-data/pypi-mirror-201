class Plane:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.origin = (0, 0)

    def set_origin(self, origin: tuple):
        self.origin = origin
