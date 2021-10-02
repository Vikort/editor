import math


class Dot:
    def __init__(self, x: int = 1, y: int = 1, z: int = 1, w: int = 1, i: float = 1.0) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.i = i

    def __str__(self):
        return "x = {}, y = {}, i = {}".format(self.x, self.y, self.i)


class Line:
    def __init__(self, begin: Dot = Dot(), end: Dot = Dot()) -> None:
        self.begin = begin
        self.end = end
        self.dots = []


def sign(number) -> int:
    if number != 0:
        return 1
    else:
        return 0


def digital_differential_analyzer(begin: Dot, end: Dot) -> list:
    dots = []
    length = max(abs(end.x - begin.x), abs(end.y - begin.y))
    dx = (end.x - begin.x) / length
    dy = (end.y - begin.y) / length
    x = begin.x + 0.5 * sign(dx)
    y = begin.y + 0.5 * sign(dy)
    dots.append(Dot(x=int(x),y=int(y)))
    # print("i = 0, x = {}, y = {}".format(x,y))
    i = 1
    while i <= length:
        x += dx
        y += dy
        dots.append(Dot(x=int(x),y=int(y)))
        # print("i = {}, x = {}, y = {}".format(i,x,y))
        i += 1
    return dots


def bresenham(begin: Dot, end: Dot) -> list:
    dots = []
    x = begin.x
    y = begin.y
    delta_x = end.x - begin.x
    delta_y = end.y - begin.y
    e = 2 * delta_y - delta_x
    dots.append(Dot(x,y))
    # print("i = 0, e = {}, x = {}, y = {}".format(e, x,y))
    if abs(delta_x) >= abs(delta_y):
        if delta_x > 0 and delta_y >= 0:
            i = 1
            while i <= delta_x:
                if e >= 0:
                    y += 1
                    e -= 2 * delta_x
                x += 1
                e += 2 * delta_y
                dots.append(Dot(x,y))
                # print("i = {}, e = {}, x = {}, y = {}".format(i, e, x, y))
                i += 1
        elif delta_x < 0 and delta_y >= 0:
            i = 1
            while i <= abs(delta_x):
                if e >= 0:
                    y += 1
                    e += 2 * delta_x
                x -= 1
                e += 2 * delta_y
                dots.append(Dot(x,y))
                # print("i = {}, e = {}, x = {}, y = {}".format(i, e, x, y))
                i += 1
        elif delta_x > 0 and delta_y <= 0:
            i = 1
            while i <= delta_x:
                if e <= 0:
                    y -= 1
                    e += 2 * delta_x
                x += 1
                e += 2 * delta_y
                dots.append(Dot(x,y))
                # print("i = {}, e = {}, x = {}, y = {}".format(i, e, x, y))
                i += 1
        elif delta_x < 0 and delta_y <= 0:
            i = 1
            while i <= abs(delta_x):
                if e <= 0:
                    y -= 1
                    e -= 2 * delta_x
                x -= 1
                e += 2 * delta_y
                dots.append(Dot(x,y))
                # print("i = {}, e = {}, x = {}, y = {}".format(i, e, x, y))
                i += 1
    else:
        e = 2 * delta_x - delta_y
        if delta_y > 0 and delta_x >= 0:
            i = 1
            while i <= delta_y:
                if e >= 0:
                    x += 1
                    e -= 2 * delta_y
                y += 1
                e += 2 * delta_x
                dots.append(Dot(x,y))
                # print("i = {}, e = {}, x = {}, y = {}".format(i, e, x, y))
                i += 1
        elif delta_y < 0 and delta_x >= 0:
            i = 1
            while i <= abs(delta_y):
                if e >= 0:
                    x += 1
                    e += 2 * delta_y
                y -= 1
                e += 2 * delta_x
                dots.append(Dot(x,y))
                # print("i = {}, e = {}, x = {}, y = {}".format(i, e, x, y))
                i += 1
        elif delta_y > 0 and delta_x <= 0:
            i = 1
            while i <= delta_y:
                if e <= 0:
                    x -= 1
                    e += 2 * delta_y
                y += 1
                e += 2 * delta_x
                dots.append(Dot(x,y))
                # print("i = {}, e = {}, x = {}, y = {}".format(i, e, x, y))
                i += 1
        elif delta_y < 0 and delta_x <= 0:
            i = 1
            while i <= abs(delta_y):
                if e <= 0:
                    x -= 1
                    e -= 2 * delta_y
                y -= 1
                e += 2 * delta_x
                dots.append(Dot(x,y))
                # print("i = {}, e = {}, x = {}, y = {}".format(i, e, x, y))
                i += 1
    return dots


def wu(begin: Dot, end: Dot) -> list:
    dots = []

    swapped = False
    
    dx = end.x - begin.x  if end.x > begin.x else begin.x - end.x
    dy = end.y - begin.y if end.y > begin.y else begin.y - end.y
    
    if dx == 0 or dy == 0:
        return bresenham(begin, end)
    
    
    if dy < dx:
        if end.x < begin.x:
            swapped = True
            end.x, begin.x = begin.x, end.x
            end.y, begin.y = begin.y, end.y

        grad = dy / dx
        if end.y < begin.y:
            grad = -grad
        intery = begin.y + grad
        dots.append(Dot(x = begin.x, y = begin.y, i = 1.0))
 
        for x in range(begin.x+1, end.x):
            i = abs(round(1 - math.modf(intery)[0], 1))
            dots.append(Dot(x = x, y = int(intery), i = math.modf(i)[0] if i != 1.0 else 1.0))
            i2 = abs(round(math.modf(intery)[0], 1))
            dots.append(Dot(x = x, y = int(intery) + 1, i = math.modf(i2)[0] if i2 != 1.0 else 1.0))
            intery += grad
        dots.append(Dot(x = end.x, y = end.y, i = 1.0))
    else:
        if end.y < begin.y:
            swapped = True
            end.x, begin.x = begin.x, end.x
            end.y, begin.y = begin.y, end.y
        
        grad = dx / dy
        if end.x < begin.x:
            grad = -grad
        interx = begin.x + grad
        dots.append(Dot(x = begin.x, y = begin.y, i = 1.0))
 
        for y in range(begin.y+1, end.y):
            i = abs(round(1 - math.modf(interx)[0], 1))
            dots.append(Dot(x = int(interx), y = y, i = math.modf(i)[0] if i != 1.0 else 1.0))
            i2 = abs(round(math.modf(interx)[0], 1))
            dots.append(Dot(x = int(interx) + 1, y = y, i = math.modf(i2)[0] if i2 != 1.0 else 1.0))
            interx += grad

        dots.append(Dot(x = end.x, y = end.y, i = 1.0))
    
    if swapped:
        end.x, begin.x = begin.x, end.x
        end.y, begin.y = begin.y, end.y

    return dots if not swapped else dots[::-1] 