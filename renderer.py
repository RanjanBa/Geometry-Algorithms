import pygame
from pygame import Vector2

class Renderer:
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
            self.surface = surface

    def renderText(self, label, pos, fontSize = 24, color = (0, 128, 0)):
        font = pygame.font.SysFont("comicsansms", fontSize)
        textRenderer = font.render(label, True, color)
        pos = Vector2(pos.x - textRenderer.get_width() // 2, pos.y - textRenderer.get_height() // 2)
        pos.y = self.surface.get_height() -  pos.y
        self.surface.blit(textRenderer, pos)

    def renderLine(self, start, end, color=(255,255,255), weight=1):
        start = Vector2(start.x, self.surface.get_height() -  start.y)
        end = Vector2(end.x, self.surface.get_height() - end.y)
        pygame.draw.line(self.surface, color, (start.x, start.y), (end.x, end.y), weight)

    def renderWireRect(self, pos, size, color = (255, 255, 255), weight=1):
        pos = Vector2(pos.x, self.surface.get_height() - pos.y)

        ul = Vector2(pos.x - size.x//2, pos.y - size.y // 2)
        ur = Vector2(pos.x + size.x//2, pos.y - size.y // 2)
        bl = Vector2(pos.x - size.x//2, pos.y + size.y // 2)
        br = Vector2(pos.x + size.x//2, pos.y + size.y // 2)
        self.renderLine(Vector2(ul.x, ul.y), Vector2(ur.x, ur.y), color, weight)
        self.renderLine(Vector2(ur.x, ur.y), Vector2(br.x, br.y), color, weight)
        self.renderLine(Vector2(br.x, br.y), Vector2(bl.x, bl.y), color, weight)
        self.renderLine(Vector2(bl.x, bl.y), Vector2(ul.x, ul.y), color, weight)

    def renderRect(self, pos, size, color = (255, 255, 255), alpha = None):
        pos = Vector2(pos.x, self.surface.get_height() - pos.y)
        if alpha is None:
            pygame.draw.rect(self.surface, color, (pos.x - size.x // 2, pos.y - size.y // 2, size.x, size.y))
        else:
            rect = pygame.Surface((size.x, size.y))
            rect.fill(color)
            rect.set_alpha(alpha)
            self.surface.blit(rect, (pos.x - size.x // 2, pos.y - size.y // 2))

    def renderPolygon(self, points, color = (255, 255, 255)):
        points = points.copy()
        for i in len(points):
            points[i].y = self.surface.get_height() - points[i].y
        pygame.draw.polygon(self.surface, color, points)

    def renderCircle(self, pos, radius, color = (255, 255, 255)):
        pos = Vector2(pos.x, self.surface.get_height() - pos.y)
        pygame.draw.circle(self.surface, color, (pos.x, pos.y), radius)
