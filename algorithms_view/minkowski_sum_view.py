import pygame as pg
from pygame import Vector2

from utilities.window import Window
from utilities.renderer import Renderer
from algorithms.minkowski_sum import minkowskiSum
from utilities.mouse import Mouse


class MinkowskiSumView(Window):
    def __init__(self):
        self.__initialize()

    def __initialize(self):
        self.__polygon1 = []
        self.__polygon2 = []
        self.__status_text = 'Minkowski Sum :'
        self.__minkowski_polygon = []

        self.__first_polygon = True
        self.__draw_polygon1 = False
        self.__draw_polygon2 = False

        self.__mouse = Mouse(
            Vector2(pg.mouse.get_pos()[0], Renderer.getInstance().surface.get_height() - pg.mouse.get_pos()[1]))

    def __calculateMinkowski(self):
        if len(self.__polygon1) < 3:
            self.__status_text = 'Minkowski Sum : length of points in polygon1 is less than 3'
            return
        if len(self.__polygon2) < 3:
            self.__status_text = 'Minkowski Sum : length of points in polygon2 is less than 3'
            return
        self.__minkowski_polygon = minkowskiSum(
            self.__polygon1, self.__polygon2)
        self.__status_text = f'Minkowski Sum : length of polygon {len(self.__minkowski_polygon)}'

    def handleEvents(self, events):
        self.__mouse.updateMouse(Vector2(
            pg.mouse.get_pos()[0], Renderer.getInstance().surface.get_height() - pg.mouse.get_pos()[1]), events)

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    if self.__first_polygon:
                        self.__draw_polygon2 = False
                        self.__draw_polygon1 = not self.__draw_polygon1
                        if self.__draw_polygon1:
                            self.__polygon1 = [
                                self.__mouse.position, self.__mouse.position]
                        else:
                            if len(self.__polygon1) > 0:
                                self.__polygon1.pop()
                    else:
                        self.__draw_polygon1 = False
                        self.__draw_polygon2 = not self.__draw_polygon2
                        if self.__draw_polygon2:
                            self.__polygon2 = [
                                self.__mouse.position, self.__mouse.position]
                        else:
                            if len(self.__polygon2) > 0:
                                self.__polygon2.pop()
                    self.__calculateMinkowski()

        if self.__mouse.leftDownClick:
            if self.__draw_polygon1:
                self.__polygon1[-1] = self.__mouse.position
                self.__polygon1.append(self.__mouse.position)
            elif self.__draw_polygon2:
                self.__polygon2[-1] = self.__mouse.position
                self.__polygon2.append(self.__mouse.position)

        if self.__mouse.scrollUp or self.__mouse.scrollDown:
            self.__first_polygon = not self.__first_polygon
            self.__draw_polygon1 = False
            self.__draw_polygon2 = False

    def render(self, debug=False):
        if self.__draw_polygon1:
            self.__polygon1[-1] = self.__mouse.position
        if self.__draw_polygon2:
            self.__polygon2[-1] = self.__mouse.position

        if len(self.__polygon1) > 2:
            Renderer.getInstance().renderPolygon(self.__polygon1)
        elif len(self.__polygon1) == 2:
            Renderer.getInstance().renderLine(
                self.__polygon1[0], self.__polygon1[1])
        elif len(self.__polygon1) == 1:
            Renderer.getInstance().renderCircle(self.__polygon1[0], 3)

        if len(self.__polygon2) > 2:
            Renderer.getInstance().renderPolygon(self.__polygon2)
        elif len(self.__polygon2) == 2:
            Renderer.getInstance().renderLine(
                self.__polygon2[0], self.__polygon2[1])
        elif len(self.__polygon2) == 1:
            Renderer.getInstance().renderCircle(self.__polygon2[0], 3)

        if len(self.__minkowski_polygon) > 2:
            Renderer.getInstance().renderPolygon(self.__minkowski_polygon)

        if self.__status_text is not None:
            pos = Vector2(Renderer.getInstance().surface.get_width(
            )//2, Renderer.getInstance().surface.get_height() - 15)
            Renderer.getInstance().renderText(self.__status_text, pos)

        if self.__first_polygon:
            Renderer.getInstance().renderText('Draw polygom 1. Scroll to draw next polygon.', Vector2(
                Renderer.getInstance().surface.get_width()//2, 15), font_size=18)
        else:
            Renderer.getInstance().renderText('Draw polygon 2. Scroll to draw next polygon.', Vector2(
                Renderer.getInstance().surface.get_width()//2, 15), font_size=18)
