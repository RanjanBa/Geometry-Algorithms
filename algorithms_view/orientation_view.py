import pygame as pg
from pygame import Vector2

from utilities.line_segment import LineSegment
from utilities.renderer import Renderer
from utilities.window import Window
from utilities.algebra_math import orientation2d
from utilities.mouse import Mouse


class OrientationView(Window):
    def __init__(self):
        self.__line = None
        self.__point = None
        self.__status_text = 'Orientation : '
        self.__start_pos = Vector2(0, 0)
        self.__end_pos = Vector2(0, 0)
        self.__mouse = Mouse(
            Vector2(pg.mouse.get_pos()[0], Renderer.getInstance().surface.get_height() - pg.mouse.get_pos()[1]))

    def __calculateOrientation(self):
        if self.__line is not None and self.__point is not None:
            orient = orientation2d(
                self.__line.start, self.__line.end, self.__point)

            if orient == 1:
                self.__status_text = 'Orientation : point is in anti-clockwise direction.'
            elif orient == -1:
                self.__status_text = 'Orientation : point is in clockwise direction.'
            else:
                self.__status_text = 'Orientation : point is colinear with line.'
        else:
            self.__status_text = 'Orientation : '

    def handleEvents(self, events):
        self.__mouse.updateMouse(Vector2(
            pg.mouse.get_pos()[0], Renderer.getInstance().surface.get_height() - pg.mouse.get_pos()[1]), events)

        if self.__mouse.leftDownClick:
            self.__start_pos = self.__mouse.position
        elif self.__mouse.leftUpClick:
            self.__end_pos = self.__mouse.position
            if self.__start_pos.distance_squared_to(self.__end_pos) > 10:
                self.__line = LineSegment(self.__start_pos, self.__end_pos)
            else:
                self.__point = self.__end_pos
            self.__calculateOrientation()

    def render(self, debug=False):
        if self.__mouse.leftDrag:
            Renderer.getInstance().renderLine(self.__start_pos, self.__mouse.position)

        if self.__line is not None:
            Renderer.getInstance().renderLine(self.__line.start, self.__line.end)
            Renderer.getInstance().renderCircle(self.__line.start, 3, color=(255, 0, 0))
            Renderer.getInstance().renderCircle(self.__line.end, 3, color=(0, 255, 0))
            Renderer.getInstance().renderText('A', self.__line.start - Vector2(0, 10))
            Renderer.getInstance().renderText('B', self.__line.end - Vector2(0, 10))

        if self.__point is not None:
            Renderer.getInstance().renderCircle(self.__point, 3, color=(0, 255, 0))
            Renderer.getInstance().renderText('C', self.__point - Vector2(0, 10))

        if self.__status_text is not None:
            pos = Vector2(Renderer.getInstance().surface.get_width(
            )//2, Renderer.getInstance().surface.get_height() - 15)
            Renderer.getInstance().renderText(self.__status_text, pos)
