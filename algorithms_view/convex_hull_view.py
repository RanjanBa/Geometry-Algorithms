import pygame as pg
from pygame import Vector2
import random

from utilities.window import Window
from utilities.renderer import Renderer
from algorithms.convex_hull import jurvisAlgo, grahamScan


class ConvexHullView(Window):
    def __init__(self):
        self.__initialize()

    def __initialize(self):
        self.__random_points = []
        self.__convex_hull = []
        self.__status_text = 'Convex Hull :'

    def __generateRandomPoints(self):
        self.__initialize()
        for i in range(100):
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            pt = Vector2(x, y)
            self.__random_points.append(pt)

    def handleEvents(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_g:
                    self.__generateRandomPoints()
                if event.key == pg.K_j:
                    if len(self.__random_points) > 0:
                        self.__convex_hull = jurvisAlgo(self.__random_points)
                        self.__status_text = 'Convex Hull : with Jurvis Algorithm.'
                if event.key == pg.K_k:
                    if len(self.__random_points) > 0:
                        self.__convex_hull = grahamScan(self.__random_points)
                        self.__status_text = 'Convex Hull : with GrahamScan Algorithm.'

    def render(self, debug=False):
        for i in range(len(self.__random_points)):
            pt = self.__random_points[i]
            Renderer.getInstance().renderCircle(pt, 3)
            if debug:
                Renderer.getInstance().renderText(
                    f'{i}', pt + Vector2(0, -10))

        cnt = len(self.__convex_hull)
        for i in range(cnt):
            pt1 = self.__convex_hull[i]
            Renderer.getInstance().renderCircle(pt1, 3, color=(0, 128, 0))
            pt2 = self.__convex_hull[(i + 1) % cnt]
            Renderer.getInstance().renderLine(pt1, pt2, color=(0, 0, 255), weight=2)

        if self.__status_text is not None:
            pos = Vector2(Renderer.getInstance().surface.get_width(
            )//2, Renderer.getInstance().surface.get_height() - 15)
            Renderer.getInstance().renderText(self.__status_text, pos)
