# Filename: bots_v_bots.py
from dlgo.agent.naive import RandomBot
from dlgo.gotypes import Player, Color, Point
from dlgo.goboard import GameState
from dlgo.utils import print_move #, print_board
from dlgo.agent.naive import RandomBot, SafetyBot, MinimaxBot
from dlgo.agent.helpers import evaluate_safety_nuanced, evaluate_territory, evaluate_safety, evaluate_high_safety

import sys
from collections import defaultdict

GRID_SIZE = 5

def play_game(bot1, bot2, game_state):
    while not game_state.is_over():
        if game_state.next_player == Player(Color.BLACK):
            move = bot1.select_move(game_state)
        else:
            move = bot2.select_move(game_state)
        game_state = game_state.apply_move(move)

    # Check if the game ended with two consecutive passes
    if game_state.last_move.is_pass and game_state.previous_state.last_move.is_pass:
        black_territory = 0
        white_territory = 0
        for row in range(1, game_state.board.num_rows + 1):
            for col in range(1, game_state.board.num_cols + 1):
                point = Point(row, col)
                color = game_state.board.get_color(point)
                if color == Color.BLACK:
                    black_territory += 1
                elif color == Color.WHITE:
                    white_territory += 1
                else:  # Empty point, check for territory
                    neighboring_colors = {game_state.board.get_color(neighbor) for neighbor in point.neighbors() if game_state.board.is_on_grid(neighbor)}
                    if Color.BLACK in neighboring_colors and Color.WHITE not in neighboring_colors:
                        black_territory += 1
                    elif Color.WHITE in neighboring_colors and Color.BLACK not in neighboring_colors:
                        white_territory += 1
       
        return Player(Color.BLACK) if black_territory > white_territory else Player(Color.WHITE)
    elif game_state.last_move.is_resign:
        return game_state.next_player.other
    else:
        return None  # It's a tie if it's not one of the above situations.


def test_bots(bots, game_state, N):
    # Initialize results dictionary with default values.
    results = defaultdict(lambda: defaultdict(int))

    for bot1 in bots:
        for bot2 in bots:
            #line = bot2._name.ljust(20)
            #print (line)
            for _ in range(N):
                sys.stdout.write('.')  # Print dot for each game.
                sys.stdout.flush()

                # Bot1 as BLACK, bot2 as WHITE.
                winner = play_game(bot1, bot2, game_state.new_game(GRID_SIZE))
                #print (str(winner))
                if winner == Player(Color.BLACK):
                    results[bot1._name][bot2._name] += 1
                elif winner == Player(Color.WHITE):
                    results[bot2._name][bot1._name] += 1

                # Bot2 as BLACK, bot1 as WHITE. Only if bots are different
                if bot1._name != bot2._name:
                    winner = play_game(bot2, bot1, game_state.new_game(GRID_SIZE))

                    if winner == Player(Color.BLACK):
                        results[bot2._name][bot1._name] += 1
                    elif winner == Player(Color.WHITE):
                        results[bot1._name][bot2._name] += 1

    print("\nResults:")
    header = "Bot" + " " * (20 - len("Bot"))
    for bot in bots:
        header += bot._name[:5].ljust(6)  # Print only first 5 chars of bot name.
    print(header)
    for bot1 in bots:
        line = bot1._name.ljust(20)
        for bot2 in bots:
            line += str(results[bot1._name][bot2._name]).ljust(6)
        print(line)

bots = [RandomBot("RandomBot"), 
        SafetyBot("Territory", evaluate_territory),
        SafetyBot("Safety", evaluate_safety),
        SafetyBot("Nuanced S", evaluate_safety_nuanced),
        SafetyBot("High S", evaluate_high_safety),
        MinimaxBot("3xNuanced", 3, evaluate_safety_nuanced)
        ]
test_bots(bots, GameState, N=10)
