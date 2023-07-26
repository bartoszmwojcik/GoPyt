#Filename:  base.py
from abc import ABC, abstractmethod
from ..gotypes import Player

class Bot(ABC):
    @abstractmethod
    def select_move(self, game_state):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def color(self):
        pass

    @abstractmethod
    def set_color(self, color: Player):
        pass

