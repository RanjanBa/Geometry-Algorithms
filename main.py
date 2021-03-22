import math
import pygame as pg
from pygame import Vector2
import random
import os, platform

from renderer import Renderer
from orientation import orient2d
from matrixAlgebra import determinant, inverse, multiplication
from minkowskiSum import Polygon, minkowskiSum
from convexHull import jurvisAlgo, grahamScan
from lineSegment import LineSegment, checkLineSegmentIntersection, intersectionPoint
from sweepLine import sweepLine, linesToSortedPoints

# colors
BLACK = (0, 0, 0)

pg.init()
SURFACE = pg.display.set_mode((800, 600))
Renderer(SURFACE)

def circlePoly(radius, step):
    points = []

    x = radius
    while x >= -radius:
        y = round(math.sqrt(radius * radius - x * x))
        points.append(Vector2(x, y))
        x -= step

    x = -radius
    while x <= radius:
        y = round(math.sqrt(radius * radius - x * x))
        points.append(Vector2(x, -y))
        x += step

    return points

def main():
    running = True
    text = None
    polygon = None

    convex_points = []
    random_points = []
    lines = []
    sweep_lines = None
    lines_to_sorted_points = None
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    running = False
                if event.key == pg.K_p:
                    random_points = []
                    convex_points = []
                    lines = []
                    sweep_lines = []
                    lines_to_sorted_points = []
                    for i in range(4):
                        x = random.randint(50, 750)
                        y = random.randint(50, 550)
                        pt = Vector2(x, y)
                        random_points.append(pt)

                    # p1 = Vector2(83, 143) # p1 = [83, 143]
                    # q1 = Vector2(462, 391) # q1 = [462, 391]
                    # p2 = Vector2(307, 213) # p2 = [307, 213]
                    # q2 = Vector2(464, 459) # q2 = [464, 459]
                    # random_points = [p1, q1, p2, q2]

                    lines = [LineSegment(random_points[0], random_points[1]), LineSegment(random_points[2], random_points[3])]
                    check = checkLineSegmentIntersection(lines[0], lines[1])
                    pt = intersectionPoint(lines[0], lines[1])
                    if pt is not None:
                        random_points.append(pt)
                        print(pt)
                    text = 'Intersect : yes' if check else 'Intersect : no'
                if event.key == pg.K_y:
                    random_points = []
                    convex_points = []
                    lines = []
                    sweep_lines = []
                    lines_to_sorted_points = []

                    # seed = random.randint(0, 1000)
                    # random.seed(seed)
                    #
                    # print('seed : ',seed)
                    for i in range(5):
                        x = random.randint(50, 750)
                        y = random.randint(50, 550)
                        pt1 = Vector2(x, y)

                        x = random.randint(50, 750)
                        y = random.randint(50, 550)
                        pt2 = Vector2(x, y)

                        random_points.append(pt1)
                        random_points.append(pt2)
                        lines.append(LineSegment(pt1, pt2, i))
                if event.key == pg.K_s:
                    if platform.system() == 'Linux':
                        os.system('clear')
                    elif platform.system() == 'Windows':
                        os.system('cls')

                    if lines is not None and len(lines) > 0:
                        lines_to_sorted_points = linesToSortedPoints(lines)
                        sweep_lines = sweepLine(lines)
                if event.key == pg.K_o:
                    random_points = []
                    convex_points = []
                    lines = []
                    sweep_lines = []
                    lines_to_sorted_points = []
                    random_points.append(Vector2(100, 150))
                    random_points.append(Vector2(400, 350))
                    random_points.append(Vector2(50, 300))
                    orient = orient2d(random_points[0], random_points[1], random_points[2])
                    text = f'Orientation : {orient}'
                if event.key == pg.K_d:
                    matrix = [[5, -1, 3], [7, 2, 4], [6, 0, 1]]
                    # matrix = [[2, 5], [3, 6]]
                    det = determinant(matrix)
                    text = f'Determinant : {det}'
                if event.key == pg.K_u:
                    # matrix = [[4, 7], [2, 6]]
                    # matrix = [[2, 4], [-4, -10]]
                    matrix = [[3, 0, 2], [2, 0, -2], [0, 1, 1]]
                    inv = inverse(matrix)
                    text = f'Inverse : {inv}'
                if event.key == pg.K_r:
                    # matrix = [[4, 7], [2, 6]]
                    # matrix = [[2, 4], [-4, -10]]
                    matrix = [[3, 0, 2], [2, 0, -2], [0, 1, 1]]
                    mult = multiplication(matrix, matrix)
                    text = f'mult : {mult}'
                if event.key == pg.K_m:
                    polygon = minkowskiSum(rectanglePoly, trianglePoly)
                if event.key == pg.K_k:
                    if len(random_points) > 0:
                        convex_points = jurvisAlgo(random_points)
                if event.key == pg.K_l:
                    if len(random_points) > 0:
                        convex_points = grahamScan(random_points)
                if event.key == pg.K_j:
                    random_points = []
                    convex_points = []
                    lines = []
                    sweep_lines = []
                    lines_to_sorted_points = []
                    random_points = [Vector2(100, 200), Vector2(100, 400), Vector2(50, 300), Vector2(50, 100), Vector2(50, 50), Vector2(500, 400), Vector2(300, 300), Vector2(500, 200), Vector2(500, 500)]
                if event.key == pg.K_g:
                    random_points = []
                    convex_points = []
                    lines = []
                    sweep_lines = []
                    lines_to_sorted_points = []
                    for i in range(100):
                        x = random.randint(50, 750)
                        y = random.randint(50, 550)
                        pt = Vector2(x, y)
                        random_points.append(pt)

        SURFACE.fill(BLACK)
        # size = 40
        # a = Vector2(1, 2)
        # b = Vector2(6, 1)
        # c = Vector2(4, 3)
        # print(f'{orient2d(a, b, c)}')
        # points = [Vector2(2, 1), Vector2(4, 1), Vector2(4, 3), Vector2(2, 3)]
        # for i in range(len(points)):
        #     points[i] = Vector2(points[i].x * size, points[i].y * size) + Vector2(250, 100)
        #
        # rectanglePoly = Polygon(points)
        #
        # points = [Vector2(20, 20), Vector2(60, 60), Vector2(20, 60)] # circlePoly(40, 3)
        #
        # for i in range(len(points)):
        #     points[i] = Vector2(points[i].x, points[i].y) + Vector2(250, 100)
        # trianglePoly = Polygon(points)
        #
        # Renderer.getInstance().renderPolygon(rectanglePoly.points)
        # Renderer.getInstance().renderPolygon(trianglePoly.points)

        if random_points is not None and len(random_points) > 0:
            for i in range(len(random_points)):
                pt = random_points[i]
                Renderer.getInstance().renderCircle(pt, 3)
                Renderer.getInstance().renderText(f'{i}', pt + Vector2(0, -10))

        if lines is not None and len(lines) > 0:
            for idx, line in enumerate(lines):
                Renderer.getInstance().renderLine(line.start, line.end, color=(0, 0, 255), weight=2)
                # mid = line.start / 2  + line.end / 2
                # mid = Vector2(int(mid.x), int(mid.y))
                # Renderer.getInstance().renderText(f'{idx}', mid, color=(0, 128, 128))

        if sweep_lines is not None and len(sweep_lines) > 0:
            for line in sweep_lines:
                Renderer.getInstance().renderLine(line.start, line.end, color=(255, 0, 0), weight=2)

        if lines_to_sorted_points is not None and len(lines_to_sorted_points) > 0:
            for pt in lines_to_sorted_points:
                color = (255, 255, 0)
                if not pt[1]:
                    color = (240, 230, 140)

                Renderer.getInstance().renderCircle(pt[0], 3, color=color)

        if convex_points is not None and len(convex_points) > 0:
            cnt = len(convex_points)
            for i in range(cnt):
                pt1 = convex_points[i]
                Renderer.getInstance().renderCircle(pt1, 3, color=(0,128,0))
                pt2 = convex_points[(i + 1) % cnt]
                Renderer.getInstance().renderLine(pt1, pt2, color=(0, 0, 255), weight=2)

        if polygon is not None:
            Renderer.getInstance().renderPolygon(polygon.points)

        if text is not None:
            Renderer.getInstance().renderText(text, Vector2(400, 40))

        pg.display.flip()
    pg.quit()

if __name__ == main():
    main()
