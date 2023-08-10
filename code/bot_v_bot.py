# Filename: bot_v_bot.py
from dlgo.agent.naive import RandomBot
from dlgo.gotypes import Player, Color
from dlgo.goboard import GameState
from dlgo.utils import print_move #, print_board
import time
#import keyboard


def main():
    # Initialize game state with an empty board
    game = GameState.new_game(9)

    bots = {
        Color.BLACK: RandomBot("black"),
        Color.WHITE: RandomBot("white"),
    }

    while not game.is_over():
        time.sleep (0.3)

        # Clear screen
        print (chr(27) + "[2J")

        # Display game state
        game.board.print_board() #(game.board)
        print("Next player: ", game.next_player)

        # Get move from current player's bot
        bot_move = bots[game.next_player.color].select_move(game)

        print_move(game.next_player, bot_move)

        # Apply bot's move to the game state
        game = game.apply_move(bot_move)
        #input ("press Eneter")

if __name__ == '__main__':
    main()
