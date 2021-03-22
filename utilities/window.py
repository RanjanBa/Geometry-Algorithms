from abc import ABC, abstractmethod


class Window(ABC):
    @abstractmethod
    def handleEvents(self, events):
        pass

    @abstractmethod
    def render(self, debug=False):
        pass
