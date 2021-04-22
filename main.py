import math
from utilities.red_black_tree import Node, RedBlackTree
import pygame as pg
import pygame_gui as pg_gui
from pygame import Vector2, Rect

from utilities.renderer import Renderer
from utilities.algebra_math import orientation2d
from utilities.algebra_math import determinant, inverse, multiplication
from utilities.line_segment import LineSegment
from utilities.window import Window

from algorithms_view.convex_hull_view import ConvexHullView
from algorithms_view.minkowski_sum_view import MinkowskiSumView
from algorithms_view.orientation_view import OrientationView
from algorithms_view.line_intersection_view import LineIntersectionView
from algorithms_view.sutherland_hodgman_view import SutherlandHodgmanView
from algorithms_view.transformation_view import TransformationView
from algorithms_view.sweep_line_view import SweepLineView
from algorithms_view.linear_transformation_view import LinearTransformationView

# colors
BLACK = (0, 0, 0)

# screen dimension
WIDTH = 800
HEIGHT = 600


pg.init()
SURFACE = pg.display.set_mode((WIDTH, HEIGHT))
Renderer(SURFACE)
gui_manager = pg_gui.UIManager((WIDTH, HEIGHT))

# windows list
windows_drop_down_menu_list = ['Convex Hull', 'Line Intersection', 'Minkowski Sum',
                               'Orientation', 'Polygon Clipping', 'Sweep Line', 'Transformation', 'Linear Transformation']

windows_list = [ConvexHullView(gui_manager), LineIntersectionView(
    gui_manager), MinkowskiSumView(gui_manager), OrientationView(gui_manager), SutherlandHodgmanView(gui_manager), SweepLineView(gui_manager), TransformationView(gui_manager), LinearTransformationView(gui_manager)]

windows_drop_down_menu = pg_gui.elements.UIDropDownMenu(windows_drop_down_menu_list,
                                                        windows_drop_down_menu_list[0], Rect(10, 10, 200, 40), gui_manager)


def cmp(a, b) -> bool:
    if a > b:
        return True
    else:
        return False

def main():
    running = True
    current_window_index = 0
    current_window = windows_list[current_window_index]
    current_window.showUI()
    clock = pg.time.Clock()
    while running:
        delta_time = clock.tick() / 1000
        events = pg.event.get()
        for event in events:
            gui_manager.process_events(event)
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
                running = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_u:
                    tree = RedBlackTree(cmp=cmp)
                    tree.insert(Node(10))
                    tree.insert(Node(20))
                    tree.insert(Node(5))
                    tree.insert(Node(30))
                    tree.insert(Node(15))
                    tree.insert(Node(9))
                    tree.insert(Node(35))
                    print(tree)
            if event.type == pg.USEREVENT:
                if event.user_type == pg_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == windows_drop_down_menu:
                    for i in range(len(windows_drop_down_menu_list)):
                        if windows_drop_down_menu_list[i] == windows_drop_down_menu.selected_option and current_window_index != i:
                            current_window_index = i
                            current_window.clear()
                            current_window.hideUI()
                            current_window = windows_list[current_window_index]
                            current_window.showUI()

        if current_window is not None and isinstance(current_window, Window):
            current_window.handleEvents(events)

        SURFACE.fill(BLACK)

        if current_window is not None and isinstance(current_window, Window):
            current_window.render()

        gui_manager.update(delta_time)
        gui_manager.draw_ui(Renderer.getInstance().surface)
        pg.display.update()

    pg.quit()


if __name__ == '__main__':
    main()
