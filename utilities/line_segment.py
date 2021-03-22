from pygame import Vector2

from utilities.algebra_math import orientation2d, determinant, inverse, multiplication


class LineSegment:
    def __init__(self, start, end, id=0):
        self.start = start
        self.end = end
        self.id = id

    def __str__(self):
        return f'Line({self.start}, {self.end}, {self.id})'

    def intersectionPoint(self, other):
        return LineSegment.lineSegmentsintersectionPoint(self, other)

    def checkIntersection(self, other):
        return LineSegment.checkSegmentIntersection(self, other)

    @staticmethod
    def checkSegmentIntersection(line1, line2):
        p1 = line1.start
        q1 = line1.end
        p2 = line2.start
        q2 = line2.end

        o1 = orientation2d(p1, q1, p2)
        o2 = orientation2d(p1, q1, q2)
        o3 = orientation2d(p2, q2, p1)
        o4 = orientation2d(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and p1.x <= p2.x <= q1.x and p1.y <= p2.y <= q1.y:
            return True

        if o2 == 0 and p1.x <= q2.x <= q1.x and p1.y <= q2.y <= q1.y:
            return True

        if o3 == 0 and p2.x <= p1.x <= q2.x and p2.y <= p1.y <= q2.y:
            return True

        if o4 == 0 and p2.x <= q1.x <= q2.x and p2.y <= q1.y <= q2.y:
            return True

        return False

    @staticmethod
    def lineSegmentsintersectionPoint(line1, line2):
        x1 = line1.start.x
        y1 = line1.start.y
        x2 = line1.end.x
        y2 = line1.end.y

        x3 = line2.start.x
        y3 = line2.start.y
        x4 = line2.end.x
        y4 = line2.end.y

        if x2 - x1 == 0 or x4 - x3 == 0:
            pass

        a1 = y2 - y1
        b1 = x1 - x2
        c1 = a1 * x1 + b1 * y1

        a2 = y4 - y3
        b2 = x3 - x4
        c2 = a2 * x3 + b2 * y3

        mat_a = [[a1, b1], [a2, b2]]
        mat_b = [[c1], [c2]]
        det = determinant(mat_a)
        if det == 0:
            print('two lines are parallel')
            return None

        inv = inverse(mat_a)
        result = multiplication(inv, mat_b)

        x = result[0][0]
        y = result[1][0]

        return Vector2(x, y)
