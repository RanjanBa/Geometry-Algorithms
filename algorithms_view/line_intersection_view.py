import pygame as pg
from pygame import Vector2

from utilities.line_segment import LineSegment
from utilities.renderer import Renderer
from utilities.window import Window
from utilities.mouse import Mouse


class LineIntersectionView(Window):
    def __init__(self, gui_manager):
        super().__init__(gui_manager)
        self.__line1 = None
        self.__line2 = None
        self.__status_text = 'Line Intersection : '
        self.__intersection_point = None
        self.__line_id = 0

        self.__start_pos = Vector2(0, 0)
        self.__end_pos = Vector2(0, 0)
        self.__mouse = Mouse(
            Vector2(pg.mouse.get_pos()[0], Renderer.getInstance().surface.get_height() - pg.mouse.get_pos()[1]))

    def __calculateIntersection(self):
        if self.__line1 is not None and self.__line2 is not None:
            check = LineSegment.checkSegmentIntersection(
                self.__line1, self.__line2)
            if check:
                self.__status_text = 'Line Segments intersect with each other.'
                self.__intersection_point = LineSegment.lineSegmentsIntersectionPoint(
                    self.__line1, self.__line2)
            else:
                self.__status_text = 'Line Segment doesn\'t intersect with each other.'
                self.__intersection_point = None

    def handleEvents(self, events):
        self.__mouse.updateMouse(Vector2(
            pg.mouse.get_pos()[0], Renderer.getInstance().surface.get_height() - pg.mouse.get_pos()[1]), events)

        if self.__mouse.leftDownClick:
            self.__start_pos = self.__mouse.position
        elif self.__mouse.leftUpClick:
            self.__end_pos = self.__mouse.position
            if self.__start_pos.distance_squared_to(self.__end_pos) > 10:
                if self.__line_id == 0:
                    self.__line1 = LineSegment(
                        self.__start_pos, self.__end_pos)
                else:
                    self.__line2 = LineSegment(
                        self.__start_pos, self.__end_pos)

            self.__calculateIntersection()
        elif self.__mouse.scrollUp:
            self.__line_id += 1
            self.__line_id %= 2
        elif self.__mouse.scrollDown:
            self.__line_id = (2 + self.__line_id - 1) % 2
            self.__line_id %= 2

    def render(self, debug=False):
        if self.__mouse.leftDrag:
            Renderer.getInstance().renderLine(self.__start_pos, self.__mouse.position)

        if self.__line1 is not None:
            Renderer.getInstance().renderLine(self.__line1.start, self.__line1.end)
            Renderer.getInstance().renderText('A', self.__line1.start - Vector2(0, 10))
            Renderer.getInstance().renderText('B', self.__line1.end - Vector2(0, 10))

        if self.__line2 is not None:
            Renderer.getInstance().renderLine(self.__line2.start, self.__line2.end)
            Renderer.getInstance().renderText('C', self.__line2.start - Vector2(0, 10))
            Renderer.getInstance().renderText('D', self.__line2.end - Vector2(0, 10))

        if self.__intersection_point is not None:
            Renderer.getInstance().renderCircle(
                self.__intersection_point, 3, color=(128, 128, 0))

        if self.__status_text is not None:
            pos = Vector2(Renderer.getInstance().surface.get_width(
            )//2, Renderer.getInstance().surface.get_height() - 15)
            Renderer.getInstance().renderText(self.__status_text, pos)

        if self.__line_id == 0:
            Renderer.getInstance().renderText('Draw AB line. Scroll to change line drawing.', Vector2(
                Renderer.getInstance().surface.get_width()//2, 15), font_size=18)
        elif self.__line_id == 1:
            Renderer.getInstance().renderText('Draw CD line. Scroll to change line drawing.', Vector2(
                Renderer.getInstance().surface.get_width()//2, 15), font_size=18)
