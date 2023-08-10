#Filename: naive.py

from .base import Bot
from ..gotypes import Player, Move, Color
import random
from .helpers import legal_moves

__all__ = ['RandomBot', 'SafetyBot']

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

class SafetyBot(Bot):
    def __init__(self, name):
        self._name = name
        self._color = None 

    def name(self):
        return self._name

    def color(self):
        return self._color

    def set_color(self, color: Player):
        self._color = color

    def select_move(self, game_state):
        best_score = float('-inf')
        best_move = None
        
        for move in legal_moves(game_state):
            # Skip eyes.
            #if game_state.is_valid_move(move) and not game_state.does_move_violate_ko(self.color, move):
                next_state = game_state.apply_move(move)
                score = self.evaluate_safety_nuanced(next_state.board)[game_state.next_player.color]
                if score > best_score:
                    best_score = score
                    best_move = move
                    
        return best_move or Move.pass_turn()

    def evaluate_safety_nuanced(self, board):
        score = {Color.BLACK: 0, Color.WHITE: 0}
        
        for _, group in board._grid.items():
            base_score = len(group.stones)
            
            # Modify the score based on the number of liberties.
            if group.num_liberties == 1:
                score[group.color] -= base_score  # heavy penalty for Atari
            elif group.num_liberties == 2:
                score[group.color] -= base_score * 0.5  # lighter penalty for potential danger
            else:
                score[group.color] += base_score  # positive score for safe groups
            
            # Additionally, add a small bonus for each liberty for groups with >2 liberties.
            if group.num_liberties > 2:
                score[group.color] += group.num_liberties * 0.5  # for instance, half a point per liberty
        
        return score
