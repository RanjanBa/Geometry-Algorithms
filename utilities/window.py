from abc import ABC, abstractmethod


class Window(ABC):
    def __init__(self, gui_manager):
        self._gui_manager = gui_manager

    @abstractmethod
    def handleEvents(self, events):
        pass

    @abstractmethod
    def render(self, debug=False):
        pass

    def showUI(self):
        pass

    def hideUI(self):
        pass

    def clear(self):
        pass
