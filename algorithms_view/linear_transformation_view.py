import math
import pygame as pg
from pygame import Vector2

from utilities.window import Window
from utilities.renderer import Renderer
from utilities.mouse import Mouse

class LinearTransformationView(Window):
    def __init__(self, gui_manager):
        super().__init__(gui_manager)
        self.__grid_size = Vector2(20, 20)
        width = Renderer.getInstance().surface.get_width()
        height = Renderer.getInstance().surface.get_height()
        self.__origin = Vector2(width//2, height//2)
        self.__mouse = Mouse(Vector2(pg.mouse.get_pos()[0], Renderer.getInstance(
        ).surface.get_height() - pg.mouse.get_pos()[1]))
        self.__mat = [1, 0, 0, 1]
        self.__idx = 0

    def handleEvents(self, events):
        self.__mouse.updateMouse((Vector2(pg.mouse.get_pos()[0], Renderer.getInstance(
        ).surface.get_height() - pg.mouse.get_pos()[1])), events)

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_0:
                    self.__idx = 0
                elif event.key == pg.K_1:
                    self.__idx = 1
                elif event.key == pg.K_2:
                    self.__idx = 2
                if event.key == pg.K_3:
                    self.__idx = 3

        if self.__mouse.scrollUp:
            self.__mat[self.__idx] += 1
        elif self.__mouse.scrollDown:
            self.__mat[self.__idx] -= 1

    def __draw_grid(self):
        width = Renderer.getInstance().surface.get_width()
        height = Renderer.getInstance().surface.get_height()
        grid_surface = pg.Surface((width, height))
        grid_surface.set_colorkey((0, 0, 0))
        grid_surface.set_alpha(75)

        color=(255, 255, 255)
        weight=1
        # left vertical lines
        x = self.__origin.x
        while True:
            x -= self.__grid_size.x
            start = Vector2(x, -10)
            end = Vector2(x, 2 * self.__origin.y + 10)
            pg.draw.line(grid_surface, color, start, end, weight)
            if x < 0:
                break

        # origin vertical line
        start = Vector2(self.__origin.x, -10)
        end = Vector2(self.__origin.x, 2 * self.__origin.y + 10)
        pg.draw.line(grid_surface, color, start, end, 2)

        # right vertical lines
        x = self.__origin.x
        while True:
            x += self.__grid_size.x
            start = Vector2(x, -10)
            end = Vector2(x, 2 * self.__origin.y + 10)
            pg.draw.line(grid_surface, color, start, end, weight)
            if x > 2 * self.__origin.x:
                break

        # bottom horizontal lines
        y = self.__origin.y
        while True:
            y -= self.__grid_size.y
            start = Vector2(-10, y)
            end = Vector2(2 * self.__origin.x + 10, y)
            pg.draw.line(grid_surface, color, start, end, weight)
            if y < 0:
                break

        # origin horizontal line
        start = Vector2(-10, self.__origin.y)
        end = Vector2(2 * self.__origin.x + 10, self.__origin.y)
        pg.draw.line(grid_surface, color, start, end, 2)

        # upper horizontal lines
        y = self.__origin.y
        while True:
            y += self.__grid_size.y
            start = Vector2(-10, y)
            end = Vector2(2 * self.__origin.x + 10, y)
            pg.draw.line(grid_surface, color, start, end, weight)
            if y > 2 * self.__origin.y:
                break
        
        Renderer.getInstance().surface.blit(grid_surface, (0, 0))

    def __draw_transform_grid(self, i_hat, j_hat):
        width = Renderer.getInstance().surface.get_width()
        height = Renderer.getInstance().surface.get_height()
        grid_surface = pg.Surface((width, height))
        grid_surface.set_colorkey((0, 0, 0))
        grid_surface.set_alpha(128)
        
        diag_distance = math.sqrt(width * width + height * height)
        half_diag_distance = diag_distance // 2 + 5

        screen_i_hat = self.__convertPointToScreenPos(i_hat)
        screen_j_hat = self.__convertPointToScreenPos(j_hat)

        weight = 1

        # parallel j_hat lines
        color = (0, 0, 255)
        # origin j_hat line
        start = self.__origin - j_hat * half_diag_distance
        end = self.__origin + j_hat * half_diag_distance

        screen_pos_start = Vector2(start.x, height - start.y)
        screen_pos_end = Vector2(end.x, height - end.y)
        pg.draw.line(grid_surface, color, screen_pos_start, screen_pos_end, 2)

        sqrt = math.sqrt(screen_i_hat.x * screen_i_hat.x + screen_i_hat.y * screen_i_hat.y)

        if sqrt != 0:
            cnt = math.ceil(half_diag_distance/sqrt)
            up_start = Vector2(start.x, start.y)
            up_end = Vector2(end.x, end.y)
            down_start = Vector2(start.x, start.y)
            down_end = Vector2(end.x, end.y)
            for i in range(1,cnt+1):
                up_start += screen_i_hat
                up_end += screen_i_hat
                screen_pos_start = Vector2(up_start.x, height - up_start.y)
                screen_pos_end = Vector2(up_end.x, height - up_end.y)
                pg.draw.line(grid_surface, color, screen_pos_start, screen_pos_end, weight)
                down_start -= screen_i_hat
                down_end -= screen_i_hat
                screen_pos_start = Vector2(down_start.x, height - down_start.y)
                screen_pos_end = Vector2(down_end.x, height - down_end.y)
                pg.draw.line(grid_surface, color, screen_pos_start, screen_pos_end, weight)

        # parrallel i_hat lines
        color = (0, 255, 0)
        # origin i_hat line
        start = self.__origin - i_hat * half_diag_distance
        end = self.__origin + i_hat * half_diag_distance

        screen_pos_start = Vector2(start.x, height - start.y)
        screen_pos_end = Vector2(end.x, height - end.y)
        pg.draw.line(grid_surface, color, screen_pos_start, screen_pos_end, 2)
        
        sqrt = math.sqrt(screen_j_hat.x * screen_j_hat.x + screen_j_hat.y * screen_j_hat.y)

        if sqrt != 0:
            cnt = math.ceil(half_diag_distance/sqrt)
            up_start = Vector2(start.x, start.y)
            up_end = Vector2(end.x, end.y)
            down_start = Vector2(start.x, start.y)
            down_end = Vector2(end.x, end.y)
            for i in range(0,cnt):
                up_start += screen_j_hat
                up_end += screen_j_hat
                screen_pos_start = Vector2(up_start.x, height - up_start.y)
                screen_pos_end = Vector2(up_end.x, height - up_end.y)
                pg.draw.line(grid_surface, color, screen_pos_start, screen_pos_end, weight)
                down_start -= screen_j_hat
                down_end -= screen_j_hat
                screen_pos_start = Vector2(down_start.x, height - down_start.y)
                screen_pos_end = Vector2(down_end.x, height - down_end.y)
                pg.draw.line(grid_surface, color, screen_pos_start, screen_pos_end, weight)
        Renderer.getInstance().surface.blit(grid_surface, (0, 0))

    def __convertPointToScreenPos(self, position):
        return Vector2(position.x * self.__grid_size.x, position.y * self.__grid_size.y)

    def __screenPosToPoint(self, position):
        return Vector2(position.x//self.__grid_size.x, position.y//self.__grid_size.y)

    def render(self, debug=False):
        self.__draw_grid()
        pt = Vector2(1, 5)
        screen_pos = self.__convertPointToScreenPos(pt)
        Renderer.getInstance().renderCircle(self.__origin + screen_pos, 3)

        i_hat = Vector2(self.__mat[0], self.__mat[1])
        j_hat = Vector2(self.__mat[2], self.__mat[3])
        self.__draw_transform_grid(i_hat, j_hat)

        screen_pos = self.__convertPointToScreenPos(Vector2(pt.x * i_hat.x + pt.y * j_hat.x, pt.x * i_hat.y + pt.y * j_hat.y))
        Renderer.getInstance().renderCircle(self.__origin + screen_pos, 3, color=(0, 0, 255))
        Renderer.getInstance().renderText(f'i hat: ({i_hat.x},{i_hat.y})', Vector2(150, 20))
        Renderer.getInstance().renderText(f'j hat: ({j_hat.x},{j_hat.y})', Vector2(500, 20))
        