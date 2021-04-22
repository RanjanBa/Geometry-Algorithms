import pygame as pg
from pygame import Vector2

from utilities.renderer import Renderer
from utilities.window import Window
from utilities.mouse import Mouse
from algorithms.sutherland_hodgman import sutherlandHodgman


class SutherlandHodgmanView(Window):
    def __init__(self, gui_manager):
        super().__init__(gui_manager)
        self.__polygon = []
        self.__clip_window = []
        self.__cliping_points = []
        self.__draw_clip_window = False
        self.__drawing_polygon = False
        self.__status_text = 'Polygon Clipping: '
        self.__mouse = Mouse(
            Vector2(pg.mouse.get_pos()[0], Renderer.getInstance().surface.get_height() - pg.mouse.get_pos()[1]))
        self.__show_only_cliping_polygon = False

    def __calculateCliping(self):
        if len(self.__polygon) < 3:
            return

        if len(self.__clip_window) < 3:
            return

        self.__cliping_points = sutherlandHodgman(
            self.__polygon, self.__clip_window)

    def handleEvents(self, events):
        self.__mouse.updateMouse(
            Vector2(pg.mouse.get_pos()[0], Renderer.getInstance().surface.get_height() - pg.mouse.get_pos()[1]), events)

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    self.__show_only_cliping_polygon = not self.__show_only_cliping_polygon
                if event.key == pg.K_d and not self.__draw_clip_window:
                    self.__drawing_polygon = not self.__drawing_polygon
                    if self.__drawing_polygon:
                        self.__clip_window = []
                        self.__cliping_points = []
                        self.__polygon = [
                            self.__mouse.position, self.__mouse.position]
                    else:
                        if len(self.__polygon) > 0:
                            self.__polygon.pop()

        if self.__mouse.leftDownClick:
            if self.__drawing_polygon:
                self.__polygon[-1] = self.__mouse.position
                self.__polygon.append(self.__mouse.position)
            if self.__draw_clip_window:
                self.__clip_window = [
                    self.__mouse.position, self.__mouse.position, self.__mouse.position, self.__mouse.position]
        elif self.__mouse.leftUpClick:
            self.__calculateCliping()

        elif self.__mouse.scrollUp or self.__mouse.scrollDown:
            self.__draw_clip_window = not self.__draw_clip_window
            self.__drawing_polygon = False

    def render(self, debug=False):
        if self.__drawing_polygon and not self.__draw_clip_window:
            self.__polygon[-1] = self.__mouse.position
        if self.__draw_clip_window:
            if len(self.__clip_window) > 0 and self.__mouse.leftDrag:
                p1 = self.__clip_window[0]
                p2 = Vector2(self.__mouse.position.x, self.__clip_window[0].y)
                p3 = self.__mouse.position
                p4 = Vector2(self.__clip_window[0].x, self.__mouse.position.y)

                self.__clip_window = [p1, p2, p3, p4]
        if not self.__show_only_cliping_polygon:
            if len(self.__polygon) > 2:
                Renderer.getInstance().renderPolygon(self.__polygon)
            elif len(self.__polygon) == 2:
                Renderer.getInstance().renderLine(
                    self.__polygon[0], self.__polygon[1])
            elif len(self.__polygon) == 1:
                Renderer.getInstance().renderCircle(self.__polygon[0], 3)

            if len(self.__clip_window) > 0:
                Renderer.getInstance().renderPolygon(
                    self.__clip_window, color=(0, 0, 255), alpha=50)

        if len(self.__cliping_points) > 2:
            Renderer.getInstance().renderPolygon(
                self.__cliping_points, color=(255, 0, 0), alpha=128)

        if self.__status_text is not None:
            pos = Vector2(Renderer.getInstance().surface.get_width(
            )//2, Renderer.getInstance().surface.get_height() - 15)
            Renderer.getInstance().renderText(self.__status_text, pos)

        if self.__draw_clip_window:
            Renderer.getInstance().renderText('Draw cliping window. Scroll to draw polygon.', Vector2(
                Renderer.getInstance().surface.get_width()//2, 15), font_size=18)
        else:
            Renderer.getInstance().renderText('Draw polygon. Scroll to draw cliping window.', Vector2(
                Renderer.getInstance().surface.get_width()//2, 15), font_size=18)
