# Filename: human_v_bot.py
from dlgo.agent.naive import RandomBot
from dlgo.gotypes import Player, Color, Move
from dlgo.goboard import GameState
from dlgo.utils import print_move, point_from_coords 
import time
#import keyboard


def main():
    # Initialize game state with an empty board
    game = GameState.new_game(9)

    bot = RandomBot("white")
    move = None

    while not game.is_over():

        # Clear screen
        print (chr(27) + "[2J")

        # Display game state
        game.board.print_board() #(game.board)
        print("Next player: ", game.next_player)
        if move is not None:
            print_move(game.next_player, move)

        if game.next_player.color == Color.BLACK:
            human_move = input ('-- ')
            point = point_from_coords(human_move.strip())
            move = Move.play(point)
        else:
            # Get move from current player's bot
            move = bot.select_move(game)

#        print_move(game.next_player, move)

        # Apply bot's move to the game state
        game = game.apply_move(move)

if __name__ == '__main__':
    main()
