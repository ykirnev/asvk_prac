import sys

class Triangle:
    def __init__(self, p1, p2, p3):
        self.points = (tuple(p1), tuple(p2), tuple(p3))

    def __abs__(self):
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        x3, y3 = self.points[2]
        area = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        return area

    def __bool__(self):
        return abs(self) > 0

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __contains__(self, other):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        def point_in_triangle(pt, v1, v2, v3):
            d1 = sign(pt, v1, v2)
            d2 = sign(pt, v2, v3)
            d3 = sign(pt, v3, v1)
            has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
            has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
            return not (has_neg and has_pos)
        if not self or not other:
            return True
        v1, v2, v3 = self.points
        for pt in other.points:
            if not point_in_triangle(pt, v1, v2, v3):
                return False
        return True

    def __and__(self, other):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        def point_in_triangle(pt, v1, v2, v3):
            d1 = sign(pt, v1, v2)
            d2 = sign(pt, v2, v3)
            d3 = sign(pt, v3, v1)
            has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
            has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
            return not (has_neg and has_pos)
        if not self or not other:
            return False
        v1, v2, v3 = self.points
        for pt in other.points:
            if point_in_triangle(pt, v1, v2, v3):
                return True
        v1, v2, v3 = other.points
        for pt in self.points:
            if point_in_triangle(pt, v1, v2, v3):
                return True
        return False

exec(sys.stdin.read())