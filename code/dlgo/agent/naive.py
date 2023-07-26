#Filename: naive.py

from .base import Bot
from ..gotypes import Player
import random
from .helpers import legal_moves

class RandomBot(Bot):
    def __init__(self, name):
        self._name = name
        self._color = None

    def select_move(self, game_state):
        # Randomly select a move from the game_state's legal moves.
        # This is just a placeholder; the actual implementation would be more complex.
        return random.choice(list(legal_moves(game_state)))

    def name(self):
        return self._name

    def color(self):
        return self._color

    def set_color(self, color: Player):
        self._color = color
