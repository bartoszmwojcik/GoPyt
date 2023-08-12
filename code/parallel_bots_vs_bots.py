# Filename: parallel_bots_v_bots.py
from dlgo.agent.naive import RandomBot
from dlgo.gotypes import Player, Color, Point
from dlgo.goboard import GameState
from dlgo.utils import print_move #, print_board
from dlgo.agent.naive import RandomBot, SafetyBot, MinimaxBot
from dlgo.agent.helpers import evaluate_safety_nuanced, evaluate_territory, evaluate_safety, evaluate_high_safety
from bots_vs_bots import play_game, bots

import sys
from collections import defaultdict
from multiprocessing import Pool, cpu_count

GRID_SIZE = 5

def bot_matchup_task(args):
    bot1, bot2, game_num, game_state = args
    print('.', end='', flush=True)  # Print dot for each game started
    winners = play_game(bot1, bot2, game_state.new_game(GRID_SIZE))
    return (bot1, bot2, winners)

def test_bots(bots, game_state, N=10, num_cores=None):
    if num_cores is None:
        num_cores = cpu_count()

    # Initialize results dictionary with default values.
    win_record = defaultdict(lambda: defaultdict(int))

    tasks = []
    for i, bot1 in enumerate(bots):
        for j, bot2 in enumerate(bots):
            for _ in range(N):
                tasks.append((bot1, bot2, _, game_state))
                if bot1._name != bot2._name:
                    task.appen((bot2, bot1, _, game_state))

    with Pool(num_cores) as pool:
        results = pool.map(bot_matchup_task, tasks)

    #win_record = {bot: {other_bot: [0, 0] for other_bot in bots} for bot in bots}
    for bot1, bot2, winner in results:
        if winner == Player(Color.BLACK):
            win_record[bot1._name][bot2._name] += 1
        elif winner == Player(Color.WHITE):
            win_record[bot2._name][bot1._name] += 1
#        if winner == GameResult.BLACK_WIN:
#            win_record[bot1][bot2][0] += 1
#        elif winner == GameResult.WHITE_WIN:
#            win_record[bot1][bot2][1] += 1

    print("\nResults:")
    header = "Bot" + " " * (20 - len("Bot"))
    for bot in bots:
        header += bot._name[:5].ljust(6)  # Print only first 5 chars of bot name.
    print(header)
    for bot1 in bots:
        line = bot1._name.ljust(20)
        for bot2 in bots:
            line += str(win_record[bot1._name][bot2._name]).ljust(6)
        print(line)
    return win_record

test_bots(bots, GameState, N=1)