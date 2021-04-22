from operator import le
from re import S
from typing import ValuesView
import pygame as pg
import pygame_gui as pg_gui
from pygame import Vector2, Rect

from utilities.algebra_math import rotateVector, scaleVector
from utilities.line_segment import LineSegment
from utilities.window import Window
from utilities.renderer import Renderer
from utilities.mouse import Mouse

class TransformationView(Window):
    LINE_TEXT = 'Line'
    RECTANGLE_TEXT = 'Rectangle'
    POLYGON_TEXT = 'Polygon'

    def __init__(self, gui_manager):
        super().__init__(gui_manager)
        self.__object_types = [TransformationView.LINE_TEXT, TransformationView.RECTANGLE_TEXT, TransformationView.POLYGON_TEXT]
        self.__origin = Vector2(0, 0)
        self.__rotation = 0

        self.__draw_object = False

        self.__line = None
        self.__rectangle = None
        self.__polygon = None

        self.__resultant_line = None
        self.__resultant_rectangle = None
        self.__resultant_polygon = None

        self.__status_text = 'Transformation: '
        self.__mouse = Mouse(
            Vector2(pg.mouse.get_pos()[0], Renderer.getInstance().surface.get_height() - pg.mouse.get_pos()[1]))

        screen_width = Renderer.getInstance().surface.get_width()
        self.__drop_down = pg_gui.elements.UIDropDownMenu(
            self.__object_types, TransformationView.LINE_TEXT, Rect(screen_width - 160, 10, 150, 40), self._gui_manager)
        self.__angle_input = pg_gui.elements.UITextEntryLine(
            Rect(screen_width - 50, 60, 60, 30), self._gui_manager)
        
        allow_chars = pg_gui.elements.UITextEntryLine._number_character_set
        allow_chars.append('-')
        self.__angle_input.set_allowed_characters(allow_chars)
        self.hideUI()

    def __changeDrawStatus(self):
        self.__draw_object = not self.__draw_object
        if self.__drop_down.selected_option == TransformationView.POLYGON_TEXT:
            if self.__draw_object:
                self.__polygon = [self.__mouse.position, self.__mouse.position]
            else:
                if self.__polygon is not None and len(self.__polygon) > 2:
                    self.__polygon.pop()
                else:
                    self.__polygon = None
        if self.__draw_object:
            self.__angle_input.disable()
        else:
            self.__angle_input.enable()
            self.__calculateRotation()

    def __changeRotation(self, delta_change = None, value = None):
        if value is None and delta_change is None:
            return
        
        if value is None:
            self.__rotation += delta_change
        elif delta_change is None:
            self.__rotation = value

        self.__calculateRotation()
        if self.__angle_input.text != str(self.__rotation):
            self.__angle_input.set_text(str(self.__rotation))

    def __calculateScale(self):
        self.__status_text = f'Transformation: scale by {self.__scale}'
        if self.__line is not None:
            start = scaleVector(self.__line.start - self.__origin, self.__scale)
            end = scaleVector(self.__line.end - self.__origin, self.__scale)
            self.__resultant_line = LineSegment(self.__origin + start, self.__origin + end)
        
        if self.__rectangle is not None:
            self.__resultant_rectangle = len(self.__rectangle) * [None]
            for i in range(len(self.__rectangle)):
                self.__resultant_rectangle[i] = scaleVector(self.__rectangle[i] - self.__origin, self.__scale) + self.__origin

        if self.__polygon is not None:
            self.__resultant_polygon = len(self.__polygon) * [None]
            for i in range(len(self.__polygon)):
                self.__resultant_polygon[i] = scaleVector(self.__polygon[i] - self.__origin, self.__scale) + self.__origin

    def __calculateRotation(self):
        self.__status_text = f'Transformation: rotation by {self.__rotation}'
        if self.__line is not None:
            start = rotateVector(self.__line.start - self.__origin, self.__rotation)
            end = rotateVector(self.__line.end - self.__origin, self.__rotation)
            self.__resultant_line = LineSegment(self.__origin + start, self.__origin + end)
        
        if self.__rectangle is not None:
            self.__resultant_rectangle = len(self.__rectangle) * [None]
            for i in range(len(self.__rectangle)):
                self.__resultant_rectangle[i] = rotateVector(self.__rectangle[i] - self.__origin, self.__rotation) + self.__origin

        if self.__polygon is not None:
            self.__resultant_polygon = len(self.__polygon) * [None]
            for i in range(len(self.__polygon)):
                self.__resultant_polygon[i] = rotateVector(self.__polygon[i] - self.__origin, self.__rotation) + self.__origin

    def handleEvents(self, events):
        self.__mouse.updateMouse(
            Vector2(pg.mouse.get_pos()[0], Renderer.getInstance().surface.get_height() - pg.mouse.get_pos()[1]), events)

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    self.__changeDrawStatus()
                if event.key == pg.K_o:
                    self.__origin = self.__mouse.position
                    self.__calculateRotation()
            if event.type == pg.USEREVENT:
                if event.user_type == pg_gui.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.__angle_input:
                    txt = self.__angle_input.text
                    if txt == '' or txt == '-':
                        txt = '0'
                    self.__changeRotation(value=int(txt))

        if self.__mouse.leftDownClick and self.__draw_object:
            if self.__drop_down.selected_option == TransformationView.LINE_TEXT:
                self.__line = LineSegment(self.__mouse.position, self.__mouse.position)
            elif self.__drop_down.selected_option == TransformationView.RECTANGLE_TEXT:
                self.__rectangle = [self.__mouse.position, self.__mouse.position, self.__mouse.position, self.__mouse.position]
            elif self.__drop_down.selected_option == TransformationView.POLYGON_TEXT:
                if self.__polygon is not None:
                    self.__polygon.append(self.__mouse.position)
        elif self.__mouse.leftDrag and self.__draw_object:
            if self.__drop_down.selected_option == TransformationView.LINE_TEXT:
                if self.__line is not None:
                    start = self.__line.start
                    self.__line = LineSegment(start, self.__mouse.position)
                    self.__calculateRotation()
            elif self.__drop_down.selected_option == TransformationView.RECTANGLE_TEXT:
                if self.__rectangle is not None:
                    pos = self.__mouse.position
                    p1 = self.__rectangle[0]
                    p2 = Vector2(pos.x, p1.y)
                    p3 = pos
                    p4 = Vector2(p1.x, pos.y)
                    
                    self.__rectangle = [p1, p2, p3, p4]
                    self.__calculateRotation()
        elif self.__mouse.scrollUp and self.__angle_input.is_focused:
            self.__changeRotation(delta_change=1)
        if self.__mouse.scrollDown and self.__angle_input.is_focused:
            self.__changeRotation(delta_change=-1)

    def render(self, debug=False):
        if self.__drop_down.selected_option == TransformationView.POLYGON_TEXT:
            if self.__draw_object and self.__polygon is not None:
                self.__polygon[-1] = self.__mouse.position

        if self.__line is not None:
            Renderer.getInstance().renderLine(self.__line.start, self.__line.end)

        if self.__rectangle is not None:
            Renderer.getInstance().renderPolygon(self.__rectangle, color=(0, 0, 255), alpha = 128)

        if self.__polygon is not None:
            if len(self.__polygon) > 2:
                Renderer.getInstance().renderPolygon(self.__polygon, color=(0, 255, 0), alpha = 128)
            elif len(self.__polygon) == 2:
                Renderer.getInstance().renderLine(self.__polygon[0], self.__polygon[1], color=(0, 255, 0))
            elif len(self.__polygon) == 1:
                Renderer.getInstance().renderCircle(self.__polygon[0], 3, color=(0, 255, 0))

        if self.__resultant_line is not None:
            Renderer.getInstance().renderLine(self.__resultant_line.start, self.__resultant_line.end)

        if self.__resultant_rectangle is not None:
            Renderer.getInstance().renderPolygon(self.__resultant_rectangle, color=(0, 0, 255), alpha = 128)

        if self.__resultant_polygon is not None:
            if len(self.__resultant_polygon) > 2:
                Renderer.getInstance().renderPolygon(self.__resultant_polygon, color=(0, 255, 0), alpha = 128)
            elif len(self.__resultant_polygon) == 2:
                Renderer.getInstance().renderLine(self.__resultant_polygon[0], self.__resultant_polygon[1], color=(0, 255, 0))
            elif len(self.__resultant_polygon) == 1:
                Renderer.getInstance().renderCircle(self.__resultant_polygon[0], 3, color=(0, 255, 0))

        Renderer.getInstance().renderCircle(self.__origin, 5, color=(255, 255, 0))

        if self.__status_text is not None:
            pos = Vector2(Renderer.getInstance().surface.get_width(
            )//2, Renderer.getInstance().surface.get_height() - 15)
            Renderer.getInstance().renderText(self.__status_text, pos)
        
        text = ''
        if self.__draw_object:
            if self.__drop_down.selected_option == TransformationView.LINE_TEXT:
                text = 'Draw Line.'
            elif self.__drop_down.selected_option == TransformationView.RECTANGLE_TEXT:
                text = 'Draw Rectangle.'
            elif self.__drop_down.selected_option == TransformationView.POLYGON_TEXT:
                text = 'Draw Polygon.'
        else:
            text = 'Press \'d\' to draw.'
        Renderer.getInstance().renderText(text, Vector2(
                Renderer.getInstance().surface.get_width()//2, 15), font_size=18)

    def showUI(self):
        self.__drop_down.show()
        self.__angle_input.show()

    def hideUI(self):
        self.__drop_down.hide()
        self.__angle_input.hide()

    def clear(self):
        self.__drop_down.kill()
        self.__angle_input.kill()
