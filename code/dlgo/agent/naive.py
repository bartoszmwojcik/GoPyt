#Filename: naive.py

from .base import Bot
from ..gotypes import Player, Move, Color
import random, sys, time
from .helpers import legal_moves

__all__ = ['RandomBot', 'SafetyBot']

MAX_SCORE = float('inf')
MIN_SCORE = float('-inf')

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
    def __init__(self, name, eval):
        self._name = name
        self._color = None
        self._eval = eval 

    def name(self):
        return self._name

    def color(self):
        return self._color

    def set_color(self, color: Player):
        self._color = color

    def select_move(self, game_state):
        best_score = MIN_SCORE
        best_moves = []
        
        for move in legal_moves(game_state):
            # Skip eyes.
            #if game_state.is_valid_move(move) and not game_state.does_move_violate_ko(self.color, move):
                next_state = game_state.apply_move(move)
                score = self._eval(next_state.board)[game_state.next_player.color]
                if score > best_score:
                    best_score = score
                    best_moves = [move]
                elif score == best_score:
                    best_moves.append(move)
                    
        return random.choice(best_moves) or Move.pass_turn()

class MinimaxBot:
    def __init__(self, name, depth, evaluation_function):
        self._name = name
        self.depth = depth
        self.evaluation_function = evaluation_function

    def select_move(self, game_state):
        return self._best_move(game_state)

    def _minimax(self, game_state, depth, is_maximizing, alpha, beta):
        #sys.stdout.write (str(depth))
        if depth == 0 or game_state.is_over():
            score = self.evaluation_function(game_state.board)
           # print (score)
            if is_maximizing:
                fx = 1
            else:
                fx = -1
            return fx * (score[Color.BLACK] - score[Color.WHITE])
        
        #legal_moves = game_state.legal_moves()
        
        if is_maximizing:
            max_eval = MIN_SCORE
            for move in legal_moves(game_state):
                new_game_state = game_state.apply_move(move)
                eval = self._minimax(new_game_state, depth-1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = MAX_SCORE
            for move in legal_moves(game_state):
                new_game_state = game_state.apply_move(move)
                eval = self._minimax(new_game_state, depth-1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
        
    def _best_move(self, game_state):
        #legal_moves = game_state.legal_moves()
        best_move = []
        best_score = MIN_SCORE #if game_state.next_player == Player(Color.BLACK) else MAX_SCORE  # BLACK maximizes, WHITE minimizes

        for move in legal_moves(game_state):
            new_game_state = game_state.apply_move(move)
            current_score = self._minimax(new_game_state, self.depth-1, game_state.next_player == Player(Color.BLACK), MIN_SCORE, MAX_SCORE)
            if game_state.next_player == Player(Color.BLACK):
                if current_score > best_score:
                    best_score = current_score
                    best_move = [move]
                elif current_score == best_score:
                    best_move.append(move)
            elif game_state.next_player == Player(Color.WHITE):
                if current_score > best_score:
                    best_score = current_score
                    best_move = [move]
                elif current_score == best_score:
                    best_move.append(move)
      #  print (best_score)
      #  time.sleep (5)
                
        return random.choice(best_move)

