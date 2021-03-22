from pygame import Vector2
from orientation import orient2d
from matrixAlgebra import determinant, inverse, multiplication
from numpy import linalg

class LineSegment:
    def __init__(self, start, end, id = 0):
        self.start = start
        self.end = end
        self.id = id

    def __str__(self):
        return f'Line({self.start}, {self.end}, {self.id})'

def checkLineSegmentIntersection(line1, line2):
    p1 = line1.start
    q1 = line1.end
    p2 = line2.start
    q2 = line2.end

    o1 = orient2d(p1, q1, p2)
    o2 = orient2d(p1, q1, q2)
    o3 = orient2d(p2, q2, p1)
    o4 = orient2d(p2, q2, q1)

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

def intersectionPoint(line1, line2):
    x1 = line1.start.x
    y1 = line1.start.y
    x2 = line1.end.x
    y2 = line1.end.y

    x3 = line2.start.x
    y3 = line2.start.y
    x4 = line2.end.x
    y4 = line2.end.y

    # s1_x = x2 - x1
    # s1_y = y2 - y1
    #
    # s2_x = x4 - x3
    # s2_y = y4 - y3
    #
    # s = (-s1_y * (x1 - x3) + s1_x * (y1 - y2)) / (-s2_x * s1_y + s1_x * s2_y)
    # t = (s2_x * (y1 - y3) - s2_y * (x1 - x3)) / (-s2_x * s1_y + s1_x * s2_y)
    # x = x1 + t * s1_x
    # y = y1 + t * s1_y

    slope1 = (y2 - y1) / (x2 - x1)
    a1 = slope1
    b1 = -1
    c1 = slope1 * x1 - y1
    print('coeff 1: ', a1, b1, c1)

    slope2 = (y4 - y3) / (x4 - x3)
    a2 = slope2
    b2 = -1
    c2 = slope2 * x3 - y3
    print('coeff 2: ', a2, b2, c2)

    mat_a = [[a1, b1], [a2, b2]]
    mat_b = [[c1], [c2]]

    if determinant(mat_a) == 0:
        print('no solution or infinitely many solution')
        return None
    inv = inverse(mat_a)
    result = multiplication(inv, mat_b)
    print(result)

    x = result[0][0]
    y = result[1][0]

    return Vector2(x, y)
