class Dot:
    def __init__(self, x: int = 1, y: int = 1, z: int = 1, w: int = 1, i: float = 1.0) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.i = i

    def __str__(self):
        return "x = {}, y = {}, i = {}".format(self.x, self.y, self.i)


def sign(number) -> int:
    if number != 0:
        return 1
    else:
        return 0
