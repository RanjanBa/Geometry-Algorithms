# TODO: not completed error active line order

import os
import platform

import pygame as pg
from pygame import Vector2


from utilities.line_segment import LineSegment
from utilities.mouse import Mouse
from utilities.renderer import Renderer
from utilities.window import Window

from algorithms.sweep_line import pairOfIntersectedLineSegment, anySegmentsIntersect


class SweepLineView(Window):
    def __init__(self, gui_manager):
        super().__init__(gui_manager)
        self.__lines = []
        self.__mouse = Mouse(Vector2(pg.mouse.get_pos()[0], Renderer.getInstance(
        ).surface.get_height() - pg.mouse.get_pos()[1]))
        self.__resultant_lines = []
        self.__status_text = 'Sweep Line: '

    def __calculateSweepLine(self):
        if platform.system() == 'Linux':
            os.system('clear')
        elif platform.system() == 'Windows':
            os.system('cls')

        self.__resultant_lines = []
        if len(self.__lines) > 1:
            # res = pairOfIntersectedLineSegment(self.__lines)
            res = anySegmentsIntersect(self.__lines)
            if res is not None:
                self.__resultant_lines = [res[0], res[1]]

    def handleEvents(self, events):
        self.__mouse.updateMouse((Vector2(pg.mouse.get_pos()[0], Renderer.getInstance(
        ).surface.get_height() - pg.mouse.get_pos()[1])), events)

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    pass

        if self.__mouse.leftDownClick:
            self.__lines.append(LineSegment(
                self.__mouse.position, self.__mouse.position))
        elif self.__mouse.leftUpClick:
            if len(self.__lines) > 0:
                start = self.__lines[-1].start
                end = self.__lines[-1].end
                if start.distance_squared_to(end) < 10:
                    self.__lines.pop()
                self.__calculateSweepLine()

    def render(self, debug=False):
        if self.__mouse.leftDrag and len(self.__lines) > 0:
            self.__lines[-1] = LineSegment(self.__lines[-1].start,
                                           self.__mouse.position)

        for i in range(len(self.__lines)):
            line = self.__lines[i]
            Renderer.getInstance().renderLine(line.start, line.end)
            Renderer.getInstance().renderText(f'{line.start.x, line.start.y}', line.start - Vector2(0, 10), font_size=14)
            Renderer.getInstance().renderText(f'{line.end.x, line.end.y}', line.end - Vector2(0, 10), font_size=14)
            Renderer.getInstance().renderText(
                f'{i}', (line.start + line.end)//2 + Vector2(0, 10), font_size=14)  

        for line in self.__resultant_lines:
            Renderer.getInstance().renderLine(line.start, line.end, color=(255, 0, 0))

        if self.__status_text is not None:
            pos = Vector2(Renderer.getInstance().surface.get_width(
            )//2, Renderer.getInstance().surface.get_height() - 15)
            Renderer.getInstance().renderText(self.__status_text, pos)