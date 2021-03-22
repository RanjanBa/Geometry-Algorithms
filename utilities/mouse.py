import pygame as pg

from pygame import Vector2


class Mouse:
    def __init__(self, pos):
        self.__pos = pos
        self.__delta_pos = Vector2(0, 0)
        self.__is_left_up_click = False
        self.__is_left_down_click = False
        self.__is_middle_up_click = False
        self.__is_middle_down_click = False
        self.__is_right_up_click = False
        self.__is_right_down_click = False
        self.__is_left_drag = False
        self.__is_middle_drag = False
        self.__is_right_drag = False
        self.__is_scroll_up = False
        self.__is_scroll_down = False

    @property
    def deltaPosition(self):
        return self.__delta_pos

    @property
    def position(self):
        return self.__pos

    @property
    def leftUpClick(self):
        return self.__is_left_up_click

    @property
    def leftDownClick(self):
        return self.__is_left_down_click

    @property
    def middleUpClick(self):
        return self.__is_middle_up_click

    @property
    def middleDownClick(self):
        return self.__is_middle_down_click

    @property
    def rightUpClick(self):
        return self.__is_right_up_click

    @property
    def rightDownClick(self):
        return self.__is_right_down_click

    @property
    def scrollUp(self):
        return self.__is_scroll_up

    @property
    def scrollDown(self):
        return self.__is_scroll_down

    @property
    def leftDrag(self):
        return self.__is_left_drag

    @property
    def middleDrag(self):
        return self.__is_middle_drag

    @property
    def rightDrag(self):
        return self.__is_right_drag

    # event.button
    # 1 - left click
    # 2 - middle click
    # 3 - right click
    # 4 - scroll up
    # 5 - scroll down

    def updateMouse(self, pos, events):
        self.resetMouseClick()
        self.__delta_pos = self.__pos - pos
        self.__pos = pos

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.__is_left_down_click = True
                    self.__is_left_drag = True
                if event.button == 2:
                    self.__is_middle_down_click = True
                    self.__is_middle_drag = True
                if event.button == 3:
                    self.__is_right_down_click = True
                    self.__is_right_drag = True
                if event.button == 4:
                    self.__is_scroll_up = True
                if event.button == 5:
                    self.__is_scroll_down = True
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.__is_left_up_click = True
                    self.__is_left_drag = False
                if event.button == 2:
                    self.__is_middle_up_click = True
                    self.__is_middle_drag = False
                if event.button == 3:
                    self.__is_right_up_click = True
                    self.__is_right_drag = False

    def resetMouseClick(self):
        self.__is_left_up_click = False
        self.__is_left_down_click = False
        self.__is_middle_up_click = False
        self.__is_middle_down_click = False
        self.__is_right_up_click = False
        self.__is_right_down_click = False
        self.__is_scroll_up = False
        self.__is_scroll_down = False
