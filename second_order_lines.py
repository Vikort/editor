from math import sqrt
from typing import ContextManager
from dot import Dot


def d_error_circle(x: float, y: float, error: float) -> tuple:
    x += 1
    y -= 1
    error += 2 * x - 2 * y + 2
    return x, y, error


def d_error_ellipse(x: float, y: float, error: float, a: int, b: int) -> tuple:
    x += 1
    y -= 1
    error += b * b * (2 * x + 1) + a * a * (1 - 2 * y)
    return x, y, error


def d_error_hyperbola(x: float, y: float, error: float, a: int, b: int) -> tuple:
    x += 1
    y += 1
    error += b * b * (2 * x + 1) - a * a * (1 + 2 * y)
    return x, y, error


def d_error_parabola(x: float, y: float, error: float, p: int) -> tuple:
    x += 1
    y += 1
    error += 1 + 2 * (y - p)
    return x, y, error


def circle(center: Dot, rDot: Dot) -> list:
    dots = []
    x = 0
    y = sqrt(pow(rDot.x - center.x, 2) + pow(rDot.y - center.y, 2))
    limit = center.y
    error = 2 - 2 * y
    dots.append(Dot(x = int(x + center.x), y = int (y + center.y)))
    dots.append(Dot(x = int(x + center.x), y = int (-y + center.y)))
    while y + center.y > limit:
        if error < 0:
            delta = 2 * error + 2 * y - 1
            if delta <= 0:
                x += 1
                error += 2 * x + 1
                dots.append(Dot(x = int(x + center.x), y = int(y + center.y)))
                dots.append(Dot(x = int(-x + center.x), y = int(-y + center.y)))
                dots.append(Dot(x = int(-x + center.x), y = int(y + center.y)))
                dots.append(Dot(x = int(x + center.x), y = int(-y + center.y)))
            else:
                x, y, error = d_error_circle(x, y, error)
                dots.append(Dot(x = int(x + center.x), y = int(y + center.y)))
                dots.append(Dot(x = int(-x + center.x), y = int(-y + center.y)))
                dots.append(Dot(x = int(-x + center.x), y = int(y + center.y)))
                dots.append(Dot(x = int(x + center.x), y = int(-y + center.y)))
        elif error == 0:
            x, y, error = d_error_circle(x, y, error)
            dots.append(Dot(x = int(x + center.x), y = int(y + center.y)))
            dots.append(Dot(x = int(-x + center.x), y = int(-y + center.y)))
            dots.append(Dot(x = int(-x + center.x), y = int(y + center.y)))
            dots.append(Dot(x = int(x + center.x), y = int(-y + center.y)))
        elif error > 0:
            delta = 2 * error - 2 * x - 1
            if delta > 0:
                y -= 1
                error += -2 * y + 1
                dots.append(Dot(x = int(x + center.x), y = int(y + center.y)))
                dots.append(Dot(x = int(-x + center.x), y = int(-y + center.y)))
                dots.append(Dot(x = int(-x + center.x), y = int(y + center.y)))
                dots.append(Dot(x = int(x + center.x), y = int(-y + center.y)))
            else:
                x, y, error = d_error_circle(x, y, error)
                dots.append(Dot(x = int(x + center.x), y = int(y + center.y)))
                dots.append(Dot(x = int(-x + center.x), y = int(-y + center.y)))
                dots.append(Dot(x = int(-x + center.x), y = int(y + center.y)))
                dots.append(Dot(x = int(x + center.x), y = int(-y + center.y)))
    return dots



def ellipse(center: Dot, endDot: Dot) -> list:
    dots = []
    x = 0
    a = endDot.x - center.x
    y = b = endDot.y - center.y
    limit = center.y
    error = a * a + b * b - 2 * a * a * b
    dots.append(Dot(x = int(x + center.x), y = int (y + center.y)))
    dots.append(Dot(x = int(x + center.x), y = int (-y + center.y)))
    while y + center.y > limit:
        if error < 0:
            delta = 2 * (error + a * a * y) - 1
            if delta <= 0:
                x += 1
                error += b * b * (2 * x + 1)
                dots.append(Dot(x = int(x + center.x), y = int(y + center.y)))
                dots.append(Dot(x = int(-x + center.x), y = int(-y + center.y)))
                dots.append(Dot(x = int(-x + center.x), y = int(y + center.y)))
                dots.append(Dot(x = int(x + center.x), y = int(-y + center.y)))
            else:
                x, y, error = d_error_ellipse(x, y, error, a, b)
                dots.append(Dot(x = int(x + center.x), y = int(y + center.y)))
                dots.append(Dot(x = int(-x + center.x), y = int(-y + center.y)))
                dots.append(Dot(x = int(-x + center.x), y = int(y + center.y)))
                dots.append(Dot(x = int(x + center.x), y = int(-y + center.y)))
        elif error == 0:
            x, y, error = d_error_ellipse(x, y, error, a, b)
            dots.append(Dot(x = int(x + center.x), y = int(y + center.y)))
            dots.append(Dot(x = int(-x + center.x), y = int(-y + center.y)))
            dots.append(Dot(x = int(-x + center.x), y = int(y + center.y)))
            dots.append(Dot(x = int(x + center.x), y = int(-y + center.y)))
        elif error > 0:
            delta = 2 * (error - b * b * x) - 1
            if delta > 0:
                y -= 1
                error += a * a * (-2 * y + 1)
                dots.append(Dot(x = int(x + center.x), y = int(y + center.y)))
                dots.append(Dot(x = int(-x + center.x), y = int(-y + center.y)))
                dots.append(Dot(x = int(-x + center.x), y = int(y + center.y)))
                dots.append(Dot(x = int(x + center.x), y = int(-y + center.y)))
            else:
                x, y, error = d_error_ellipse(x, y, error, a, b)
                dots.append(Dot(x = int(x + center.x), y = int(y + center.y)))
                dots.append(Dot(x = int(-x + center.x), y = int(-y + center.y)))
                dots.append(Dot(x = int(-x + center.x), y = int(y + center.y)))
                dots.append(Dot(x = int(x + center.x), y = int(-y + center.y)))
    return dots


def hyperbola(begin: Dot, end: Dot) -> list:
    dots = []
    y = 0
    x = a = end.x - begin.x
    b = end.y - begin.y
    limit = b
    error = b * b + 2 * a * b * b + a * a
    dots.append(Dot(x = int(x + begin.x), y = int (y + begin.y)))
    # dots.append(Dot(x = int(x + begin.x), y = int (-y + begin.y)))
    while y < limit:
        if error < 0:
            delta = 2 * (error + y * a * a) + a * a
            if delta <= 0:
                x += 1
                error += b * b * (2 * x + 1)
                dots.append(Dot(x = int(x + begin.x), y = int(y + begin.y)))
                dots.append(Dot(x = int(-x + begin.x), y = int(-y + begin.y)))
                dots.append(Dot(x = int(-x + begin.x), y = int(y + begin.y)))
                dots.append(Dot(x = int(x + begin.x), y = int(-y + begin.y)))
            else:
                x, y, error = d_error_hyperbola(x, y, error, a, b)
                dots.append(Dot(x = int(x + begin.x), y = int(y + begin.y)))
                dots.append(Dot(x = int(-x + begin.x), y = int(-y + begin.y)))
                dots.append(Dot(x = int(-x + begin.x), y = int(y + begin.y)))
                dots.append(Dot(x = int(x + begin.x), y = int(-y + begin.y)))
        elif error == 0:
            x, y, error = d_error_hyperbola(x, y, error, a, b)
            dots.append(Dot(x = int(x + begin.x), y = int(y + begin.y)))
            dots.append(Dot(x = int(-x + begin.x), y = int(-y + begin.y)))
            dots.append(Dot(x = int(-x + begin.x), y = int(y + begin.y)))
            dots.append(Dot(x = int(x + begin.x), y = int(-y + begin.y)))
        elif error > 0:
            delta = 2 * (error - b * b * x) - b * b
            if delta > 0:
                y += 1
                error -= a * a * (2 * y + 1)
                dots.append(Dot(x = int(x + begin.x), y = int(y + begin.y)))
                dots.append(Dot(x = int(-x + begin.x), y = int(-y + begin.y)))
                dots.append(Dot(x = int(-x + begin.x), y = int(y + begin.y)))
                dots.append(Dot(x = int(x + begin.x), y = int(-y + begin.y)))
            else:
                x, y, error = d_error_hyperbola(x, y, error, a, b)
                dots.append(Dot(x = int(x + begin.x), y = int(y + begin.y)))
                dots.append(Dot(x = int(-x + begin.x), y = int(-y + begin.y)))
                dots.append(Dot(x = int(-x + begin.x), y = int(y + begin.y)))
                dots.append(Dot(x = int(x + begin.x), y = int(-y + begin.y)))
    return dots


def parabola(begin: Dot, end: Dot) -> list:
    dots = []
    is_swapped = False
    y = x = 0
    delta_y = end.y - begin.y
    delta_x = end.x - begin.x
    if delta_x < 0:
        is_swapped = True
    p = int(delta_y * delta_y / 2 / abs(delta_x))
    limit = abs(delta_x)
    error = 1 - 2 * p
    if not is_swapped:
        dots.append(Dot(x = int(x + begin.x), y = int (y + begin.y)))
    else:
        dots.append(Dot(x = int(x + begin.x), y = int (-y + begin.y)))
    while x < limit:
        if error < 0:
            delta = 2 * (error + p)
            if delta <= 0:
                y += 1
                error += 2 * y + 1
                if not is_swapped:
                    dots.append(Dot(x = int(x + begin.x), y = int(y + begin.y)))
                    dots.append(Dot(x = int(x + begin.x), y = int(-y + begin.y)))
                else:
                    dots.append(Dot(x = int(-x + begin.x), y = int(-y + begin.y)))
                    dots.append(Dot(x = int(-x + begin.x), y = int(y + begin.y)))
            else:
                x, y, error = d_error_parabola(x, y, error, p)
                if not is_swapped:
                    dots.append(Dot(x = int(x + begin.x), y = int(y + begin.y)))
                    dots.append(Dot(x = int(x + begin.x), y = int(-y + begin.y)))
                else:
                    dots.append(Dot(x = int(-x + begin.x), y = int(-y + begin.y)))
                    dots.append(Dot(x = int(-x + begin.x), y = int(y + begin.y)))
        elif error == 0:
            x, y, error = d_error_parabola(x, y, error, p)
            if not is_swapped:
                dots.append(Dot(x = int(x + begin.x), y = int(y + begin.y)))
                dots.append(Dot(x = int(x + begin.x), y = int(-y + begin.y)))
            else:
                dots.append(Dot(x = int(-x + begin.x), y = int(-y + begin.y)))
                dots.append(Dot(x = int(-x + begin.x), y = int(y + begin.y)))
        elif error > 0:
            delta = 2 * (error - y) - 1
            if delta > 0:
                x += 1
                error -= 2 * p
                if not is_swapped:
                    dots.append(Dot(x = int(x + begin.x), y = int(y + begin.y)))
                    dots.append(Dot(x = int(x + begin.x), y = int(-y + begin.y)))
                else:
                    dots.append(Dot(x = int(-x + begin.x), y = int(-y + begin.y)))
                    dots.append(Dot(x = int(-x + begin.x), y = int(y + begin.y)))
            else:
                x, y, error = d_error_parabola(x, y, error, p)
                if not is_swapped:
                    dots.append(Dot(x = int(x + begin.x), y = int(y + begin.y)))
                    dots.append(Dot(x = int(x + begin.x), y = int(-y + begin.y)))
                else:
                    dots.append(Dot(x = int(-x + begin.x), y = int(-y + begin.y)))
                    dots.append(Dot(x = int(-x + begin.x), y = int(y + begin.y)))
    return dots
