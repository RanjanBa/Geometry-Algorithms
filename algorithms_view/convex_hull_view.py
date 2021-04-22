import pygame as pg
import pygame_gui as pg_gui
from pygame import Vector2, Rect
import random

from utilities.window import Window
from utilities.renderer import Renderer
from algorithms.convex_hull import jurvisAlgo, grahamScan


class ConvexHullView(Window):
    __JURVIS = 'Jurvis Algo'
    __GRAHAM = 'Graham Scan Alog'

    def __init__(self, gui_manager):
        super().__init__(gui_manager)
        self.__adding_point_activate = False

        self.__drop_down = pg_gui.elements.UIDropDownMenu(
            [ConvexHullView.__JURVIS, ConvexHullView.__GRAHAM], ConvexHullView.__JURVIS, Rect(Renderer.getInstance().surface.get_width() - 210, 10, 200, 40), self._gui_manager)
        self.__initializePoints()

        self.hideUI()

    def __initializePoints(self):
        self.__random_points = []
        self.__convex_hull = []
        self.__status_text = 'Convex Hull :'

    def __generateRandomPoints(self):
        self.__initializePoints()
        for i in range(100):
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            pt = Vector2(x, y)
            self.__random_points.append(pt)

    def __calculateConvexHul(self):
        if len(self.__random_points) > 0:
            if self.__drop_down.selected_option == ConvexHullView.__JURVIS:
                self.__convex_hull = jurvisAlgo(self.__random_points)
                self.__status_text = 'Convex Hull : with Jurvis Algorithm.'
            elif self.__drop_down.selected_option == ConvexHullView.__GRAHAM:
                self.__convex_hull = grahamScan(self.__random_points)
                self.__status_text = 'Convex Hull : with GrahamScan Algorithm.'

    def handleEvents(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_g:
                    self.__generateRandomPoints()
                    self.__calculateConvexHul()
                if event.key == pg.K_a:
                    self.__adding_point_activate = not self.__adding_point_activate
                if event.key == pg.K_c:
                    self.__initializePoints()
            if event.type == pg.USEREVENT:
                if event.user_type == pg_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.__drop_down:
                    self.__calculateConvexHul()

            if self.__adding_point_activate and event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = Vector2(pg.mouse.get_pos()[
                                    0], pg.mouse.get_pos()[1])
                pos = Vector2(mouse_pos.x, Renderer.getInstance(
                ).surface.get_height() - mouse_pos.y)
                self.__random_points.append(pos)
                self.__calculateConvexHul()

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

        if self.__adding_point_activate:
            Renderer.getInstance().renderText(
                'Press \'left click\' to add point and Press \'c\' to clear all points.', Vector2(
                    Renderer.getInstance().surface.get_width()//2, 15), font_size=18)
        else:
            Renderer.getInstance().renderText(
                'Press \'a\' to add point and Press \'c\' to clear all points.', Vector2(
                    Renderer.getInstance().surface.get_width()//2, 15), font_size=18)

    def showUI(self):
        self.__drop_down.show()

    def hideUI(self):
        self.__drop_down.hide()

    def clear(self):
        self.__drop_down.kill()
