# TODO: need to update both algorithm for points on outer line i.e orientation == 0
from functools import cmp_to_key

from utilities.algebra_math import orientation2d


def __cmp(a, b):
    if a.x == b.x:
        return a.y - b.y
    return a.x - b.x


def jurvisAlgo(points):
    length = len(points)

    if length <= 1:
        return points

    left = 0
    for i in range(1, length):
        if points[i].x < points[left].x:
            left = i

    hull = []
    p = left
    while True:
        hull.append(points[p])

        # q = 0 if p !=  0 else 1
        q = (p + 1) % length
        for i in range(length):
            if i == p:
                continue
            orient = orientation2d(points[p], points[q], points[i])
            if orient > 0:
                q = i
        p = q

        if p == left:
            break

    return hull


def grahamScan(points):
    length = len(points)

    points = sorted(points, key=cmp_to_key(__cmp))
    # print(points)

    up = [0]
    down = [0]

    for i in range(1, length):
        orient = orientation2d(points[0], points[-1], points[i])
        if i == length - 1 or orient == 1:
            while len(up) >= 2 and orientation2d(points[up[-2]], points[up[-1]], points[i]) >= 0:
                up.pop()
            # while len(up) > 2 and orientation2d(up[-2], up[-1], points[i]) == -1:
            up.append(i)
        if i == length - 1 or orient == -1:
            while len(down) >= 2 and orientation2d(points[down[-2]], points[down[-1]], points[i]) <= 0:
                down.pop()
            down.append(i)

    # hull = [points[0], points[-1]]

    hull = []
    for idx in up:
        hull.append(points[idx])
    down.reverse()
    down = down[1:-1]
    for idx in down:
        hull.append(points[idx])

    return hull
