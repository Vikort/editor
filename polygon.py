from line import Line


class Polygon:
    def __init__(self, edges_count: int = 0):
        self.dots = []
        self.edges_count = edges_count

    def get_edges(self):
        if 0 <= len(self.dots) < 2:
            return self.dots
        if len(self.dots) >= 2:
            lines = []
            for i, dot in enumerate(self.dots):
                if i == 0:
                    continue
                lines.append(Line(self.dots[i-1], dot))
            return lines


class Triangle(Polygon):
    def __init__(self):
        super().__init__(3)


class Quadrangle(Polygon):
    def __init__(self):
        super().__init__(4)


