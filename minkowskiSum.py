class Polygon:
    def __init__(self, points):
        self.points = points

def rotate(points, rot):
    if len(points) <= 0:
        return
    for i in range(rot):
        points.append(points[0])
        points.pop(0)

    return points

def reorderPolygon(points):
    pos = 0;
    for i in range(len(points)):
        if points[i].y < points[pos].y or (points[i].y == points[pos].y and points[i].x < points[pos].x):
            pos = i;

    newPoints = rotate(points, pos)
    return newPoints

def cross(vec1, vec2):
    return vec1.x * vec2.y - vec1.y * vec2.x

def minkowskiSum(polygon1, polygon2):
    points1 = reorderPolygon(polygon1.points)
    points2 = reorderPolygon(polygon2.points)

    print('poly 1 old')
    for p in polygon1.points:
        print(p)

    print('poly 1')
    for p in points1:
        print(p)

    print('poly 2 old')
    for p in polygon2.points:
        print(p)
    print('poly 2')
    for p in points2:
        print(p)

    points1.append(points1[0])
    points1.append(points1[1])

    points2.append(points2[0])
    points2.append(points2[1])

    points = []
    i = 0
    j = 0
    while i < (len(points1) - 2) or j < (len(points2) - 2):
        vec = points1[i] + points2[j]
        points.append(vec)
        if(i + 1 >= len(points1) or j + 1 >= len(points2)):
            break
        cr = cross(points1[i+1] - points1[i], points2[j+1] - points2[j])
        if cr >= 0:
            i += 1
        if cr <= 0:
            j += 1

    return Polygon(points)
