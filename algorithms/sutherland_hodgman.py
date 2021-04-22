"""
    Contains algorithms for cliping polygon with rectangle window
"""

# from typing import
from pygame import Vector2, Rect
import pygame_gui
from utilities.line_segment import LineSegment

# rect = (top, right, bottom, left)

INF = 1000000000


def leftClip(polygon, rect):
    min_x = min(rect[0].x, rect[1].x, rect[2].x, rect[3].x)
    min_y = min(rect[0].y, rect[1].y, rect[2].y, rect[3].y)
    max_x = max(rect[0].x, rect[1].x, rect[2].x, rect[3].x)
    max_y = max(rect[0].y, rect[1].y, rect[2].y, rect[3].y)

    newPolygon = [Vector2(pt.x, pt.y) for pt in polygon]
    length = len(newPolygon)
    points = []
    # left clipping
    for i in range(length):
        pt1 = newPolygon[i]
        pt2 = newPolygon[(i+1) % length]

        pt1_inside = False
        if min_x <= pt1.x:
            pt1_inside = True

        pt2_inside = False
        if min_x <= pt2.x:
            pt2_inside = True

        if pt1_inside:
            if pt2_inside:
                points.append(pt2)
            else:
                line1 = LineSegment(pt1, pt2)
                line2 = LineSegment(Vector2(min_x, -INF),
                                    Vector2(min_x, INF))

                if line1.checkIntersection(line2):
                    intersection_pt = line1.intersectionPoint(line2)
                    points.append(intersection_pt)
        else:
            if pt2_inside:
                line1 = LineSegment(pt1, pt2)
                line2 = LineSegment(Vector2(min_x, -INF),
                                    Vector2(min_x, INF))

                if line1.checkIntersection(line2):
                    intersection_pt = line1.intersectionPoint(line2)
                    points.append(intersection_pt)
                    points.append(pt2)
            else:
                continue
    return points


def rightClip(polygon, rect):
    min_x = min(rect[0].x, rect[1].x, rect[2].x, rect[3].x)
    min_y = min(rect[0].y, rect[1].y, rect[2].y, rect[3].y)
    max_x = max(rect[0].x, rect[1].x, rect[2].x, rect[3].x)
    max_y = max(rect[0].y, rect[1].y, rect[2].y, rect[3].y)

    newPolygon = [Vector2(pt.x, pt.y) for pt in polygon]
    length = len(newPolygon)
    points = []
    # right clipping
    for i in range(length):
        pt1 = newPolygon[i]
        pt2 = newPolygon[(i+1) % length]

        pt1_inside = False
        if pt1.x <= max_x:
            pt1_inside = True

        pt2_inside = False
        if pt2.x <= max_x:
            pt2_inside = True

        if pt1_inside:
            if pt2_inside:
                points.append(pt2)
            else:
                line1 = LineSegment(pt1, pt2)
                line2 = LineSegment(Vector2(max_x, -INF),
                                    Vector2(max_x, INF))

                if line1.checkIntersection(line2):
                    intersection_pt = line1.intersectionPoint(line2)
                    points.append(intersection_pt)
        else:
            if pt2_inside:
                line1 = LineSegment(pt1, pt2)
                line2 = LineSegment(Vector2(max_x, -INF),
                                    Vector2(max_x, INF))

                if line1.checkIntersection(line2):
                    intersection_pt = line1.intersectionPoint(line2)
                    points.append(intersection_pt)
                    points.append(pt2)
            else:
                continue

    return points


def bottomClip(polygon, rect):
    min_x = min(rect[0].x, rect[1].x, rect[2].x, rect[3].x)
    min_y = min(rect[0].y, rect[1].y, rect[2].y, rect[3].y)
    max_x = max(rect[0].x, rect[1].x, rect[2].x, rect[3].x)
    max_y = max(rect[0].y, rect[1].y, rect[2].y, rect[3].y)

    newPolygon = [Vector2(pt.x, pt.y) for pt in polygon]
    length = len(newPolygon)
    points = []

    # bottom clipping
    for i in range(length):
        pt1 = newPolygon[i]
        pt2 = newPolygon[(i+1) % length]

        pt1_inside = False
        if min_y <= pt1.y:
            pt1_inside = True

        pt2_inside = False
        if min_y <= pt2.y:
            pt2_inside = True

        if pt1_inside:
            if pt2_inside:
                points.append(pt2)
            else:
                line1 = LineSegment(pt1, pt2)
                line2 = LineSegment(Vector2(-INF, min_y),
                                    Vector2(INF, min_y))

                if line1.checkIntersection(line2):
                    intersection_pt = line1.intersectionPoint(line2)
                    points.append(intersection_pt)
        else:
            if pt2_inside:
                line1 = LineSegment(pt1, pt2)
                line2 = LineSegment(Vector2(-INF, min_y),
                                    Vector2(INF, min_y))

                if line1.checkIntersection(line2):
                    intersection_pt = line1.intersectionPoint(line2)
                    points.append(intersection_pt)
                    points.append(pt2)
            else:
                continue

    return points


def upperClip(polygon, rect):
    min_x = min(rect[0].x, rect[1].x, rect[2].x, rect[3].x)
    min_y = min(rect[0].y, rect[1].y, rect[2].y, rect[3].y)
    max_x = max(rect[0].x, rect[1].x, rect[2].x, rect[3].x)
    max_y = max(rect[0].y, rect[1].y, rect[2].y, rect[3].y)

    newPolygon = [Vector2(pt.x, pt.y) for pt in polygon]
    length = len(newPolygon)
    points = []

    # upper clipping
    for i in range(length):
        pt1 = newPolygon[i]
        pt2 = newPolygon[(i+1) % length]

        pt1_inside = False
        if pt1.y <= max_y:
            pt1_inside = True

        pt2_inside = False
        if pt2.y <= max_y:
            pt2_inside = True

        if pt1_inside:
            if pt2_inside:
                points.append(pt2)
            else:
                line1 = LineSegment(pt1, pt2)
                line2 = LineSegment(Vector2(-INF, max_y),
                                    Vector2(INF, max_y))

                if line1.checkIntersection(line2):
                    intersection_pt = line1.intersectionPoint(line2)
                    points.append(intersection_pt)
        else:
            if pt2_inside:
                line1 = LineSegment(pt1, pt2)
                line2 = LineSegment(Vector2(-INF, max_y),
                                    Vector2(INF, max_y))

                if line1.checkIntersection(line2):
                    intersection_pt = line1.intersectionPoint(line2)
                    points.append(intersection_pt)
                    points.append(pt2)
            else:
                continue

    return points


def sutherlandHodgman(polygon, rect):
    points = leftClip(polygon, rect)
    points = rightClip(points, rect)
    points = bottomClip(points, rect)
    points = upperClip(points, rect)
    return points
