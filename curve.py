from dot import Dot
import numpy as np


class Curve:
    def __init__(self):
        self.boundary_points = dict()

    def get_boundary_dots(self):
        res = []
        for bd in self.boundary_points:
            res.append(self.boundary_points[bd][1])
        return res


def sum_matrix(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    if left.shape[0] != right.shape[0] and left.shape[1] != right.shape[1]:
        raise Exception('can\'t sum matrix')
    res = np.zeros(left.shape)
    for i in range(len(left)):
        a = left[i]
        b = right[i]
        c = res[i]
        for j in range(len(a)):
            c[j] = a[j] + b[j]
    return res


def mult_matrix(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    res = np.zeros((left.shape[0], right.shape[1]))
    if left.shape[1] != right.shape[0]:
        raise Exception('can\'t mult matrix')
    for i in range(left.shape[0]):
        for j in range(right.shape[1]):
            for k in range(right.shape[0]):
                res[i][j] += left[i][k] * right[k][j]
    return res


def transpose_matrix(matrix: np.ndarray) -> np.ndarray:
    res = np.zeros(matrix.shape)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            res[i][j] = matrix[j][i]
    return res


def hermite_shape(dots) -> list:
    res_dots = []
    hermite_matrix = np.array([
        [2, -2, 1, 1],
        [-3, 3, -2, -1],
        [0, 0, 1, 0],
        [1, 0, 0, 0]
    ])
    dots_matrix = np.array([
        [dots[0].x, dots[0].y],
        [dots[1].x, dots[1].y],
        [dots[2].x, dots[2].y],
        [dots[3].x, dots[3].y]
    ])
    coefficient = mult_matrix(hermite_matrix, dots_matrix)
    for t in range(101):
        t_matrix = np.array([[pow(t / 100, 3), pow(t / 100, 2), t / 100, 1]])
        dot_matrix = mult_matrix(t_matrix, coefficient)
        res_dots.append(Dot(x=dot_matrix[0][0], y=dot_matrix[0][1]))
    return res_dots


def bezier_shape(dots) -> list:
    # ((x_3 - x_1) * (y_2 - y_1)) == (y_3 - y_1) * (x_2 - x_1)
    res_dots = []
    hermite_matrix = np.array([
        [-1, 3, -3, 1],
        [3, -6, 3, 0],
        [-3, 3, 0, 0],
        [1, 0, 0, 0]
    ])
    dots_matrix = np.array([
        [dots[0].x, dots[0].y],
        [dots[1].x, dots[1].y],
        [dots[2].x, dots[2].y],
        [dots[3].x, dots[3].y]
    ])
    coefficient = mult_matrix(hermite_matrix, dots_matrix)
    for t in range(101):
        t_matrix = np.array([[pow(t / 100, 3), pow(t / 100, 2), t / 100, 1]])
        dot_matrix = mult_matrix(t_matrix, coefficient)
        res_dots.append(Dot(x=dot_matrix[0][0], y=dot_matrix[0][1]))
    return res_dots


def b_spline(dots: list) -> list:
    res_dots = []
    hermite_matrix = np.array([
        [-1, 3, -3, 1],
        [3, -6, 3, 0],
        [-3, 0, 3, 0],
        [1, 4, 1, 0]
    ])
    for i in range(1, len(dots) - 2):
        dots_matrix = np.array([
            [dots[i - 1].x, dots[i - 1].y],
            [dots[i].x, dots[i].y],
            [dots[i + 1].x, dots[i + 1].y],
            [dots[i + 2].x, dots[i + 2].y]
        ])
        coefficient = mult_matrix(hermite_matrix, dots_matrix)
        for t in range(11):
            t_matrix = np.array([[pow(t / 10, 3) / 6, pow(t / 10, 2) / 6, t / 10 / 6, 1 / 6]])
            dot_matrix = mult_matrix(t_matrix, coefficient)
            res_dots.append(Dot(x=dot_matrix[0][0], y=dot_matrix[0][1]))
    return res_dots
