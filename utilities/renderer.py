import pygame as pg
from pygame import Vector2


class Renderer:
    """
        Renderer is a singleton class. It uses pygame libray to draw objects and text.
    """
    __instance = None

    @staticmethod
    def getInstance():
        if Renderer.__instance == None:
            raise Exception('This class is not initialized')
        return Renderer.__instance

    def __init__(self, surface):
        if Renderer.__instance != None:
            raise Exception('This class is singleton')
        else:
            Renderer.__instance = self
            self.__surface = surface

    @property
    def surface(self):
        return self.__surface

    def renderText(self, label, pos, font_size=24, color=(0, 128, 0), text_align='center'):
        font = pg.font.SysFont("comicsansms", font_size)
        textRenderer = font.render(label, True, color)

        if text_align == 'center':
            pos = Vector2(pos.x - textRenderer.get_width() // 2,
                          pos.y + textRenderer.get_height() // 2)
        pos.y = self.__surface.get_height() - pos.y
        self.__surface.blit(textRenderer, pos)

    def renderLine(self, start, end, color=(255, 255, 255), weight=1):
        start = Vector2(start.x, self.__surface.get_height() - start.y)
        end = Vector2(end.x, self.__surface.get_height() - end.y)
        pg.draw.line(self.__surface, color,
                     (start.x, start.y), (end.x, end.y), weight)

    def renderWireRect(self, pos, size, color=(255, 255, 255), weight=1):
        pos = Vector2(pos.x, self.__surface.get_height() - pos.y)

        ul = Vector2(pos.x - size.x//2, pos.y - size.y // 2)
        ur = Vector2(pos.x + size.x//2, pos.y - size.y // 2)
        bl = Vector2(pos.x - size.x//2, pos.y + size.y // 2)
        br = Vector2(pos.x + size.x//2, pos.y + size.y // 2)
        self.renderLine(Vector2(ul.x, ul.y), Vector2(
            ur.x, ur.y), color, weight)
        self.renderLine(Vector2(ur.x, ur.y), Vector2(
            br.x, br.y), color, weight)
        self.renderLine(Vector2(br.x, br.y), Vector2(
            bl.x, bl.y), color, weight)
        self.renderLine(Vector2(bl.x, bl.y), Vector2(
            ul.x, ul.y), color, weight)

    def renderRect(self, pos, size, color=(255, 255, 255), alpha=None):
        pos = Vector2(pos.x, self.__surface.get_height() - pos.y)
        if alpha is None:
            pg.draw.rect(self.__surface, color, (pos.x -
                                                 size.x // 2, pos.y - size.y // 2, size.x, size.y))
        else:
            surf = pg.Surface((size.x, size.y))
            surf.set_colorkey((0, 0, 0))
            surf.set_alpha(alpha)
            pg.draw.rect(surf, color, (0, 0, size.x, size.y))
            self.__surface.blit(
                surf, (pos.x - size.x // 2, pos.y - size.y // 2))

    def renderPolygon(self, points, color=(255, 255, 255), alpha=None):
        newPoints = [Vector2(pt.x, pt.y) for pt in points]
        for i in range(len(newPoints)):
            newPoints[i].y = self.__surface.get_height() - newPoints[i].y
        if alpha is None:
            pg.draw.polygon(self.__surface, color, newPoints)
        else:
            min_x = newPoints[0].x
            min_y = newPoints[0].y
            max_x = newPoints[0].x
            max_y = newPoints[0].y

            for pt in newPoints:
                if pt.x < min_x:
                    min_x = pt.x

                if pt.y < min_y:
                    min_y = pt.y

                if pt.x > max_x:
                    max_x = pt.x

                if pt.y > max_y:
                    max_y = pt.y

            surf = pg.Surface((max_x-min_x, max_y - min_y))
            surf.set_colorkey((0, 0, 0))
            surf.set_alpha(alpha)
            pg.draw.polygon(
                surf, color, [(pt.x - min_x, pt.y - min_y) for pt in newPoints])
            self.__surface.blit(surf, (min_x, min_y))

    def renderCircle(self, pos, radius, color=(255, 255, 255), alpha=None):
        pos = Vector2(pos.x, self.__surface.get_height() - pos.y)
        if alpha is None:
            pg.draw.circle(self.__surface, color, (pos.x, pos.y), radius)
        else:
            surf = pg.Surface((2 * radius, 2 * radius))
            surf.set_colorkey((0, 0, 0))
            surf.set_alpha(alpha)
            pg.draw.circle(surf, color, (radius, radius), radius)
            self.__surface.blit(surf, (pos.x - radius, pos.y - radius))
