from pygame import Vector2
from matrixAlgebra import determinant

def orient2d(a, b, c):
    matrix = [[a.x, a.y, 1], [b.x, b.y, 1], [c.x, c.y, 1]]
    det = determinant(matrix)
    if det > 0:
        return 1 # anticlockwise
    elif det < 0:
        return -1 # clockwise
    else:
        return 0
