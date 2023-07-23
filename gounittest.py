# Filename: gounittest.py

import unittest
from gotypes import Color, Player, Point, Move
from goboard1 import Board, GameState

class TestBoard(unittest.TestCase):
    def test_initialization(self):
        board = Board(num_rows=19, num_cols=19)
        self.assertEqual(board._grid, {})  # Board should start empty

    def test_place_stone(self):
        board = Board(num_rows=19, num_cols=19)
        board.place_stone(Player(Color.BLACK), Point(row=1, col=1))
        self.assertIsNotNone(board._grid.get(Point(row=1, col=1)))  # Stone should be placed

    def test_capture(self):
        board = Board(num_rows=19, num_cols=19)
        board.place_stone(Player(Color.BLACK), Point(row=1, col=1))
        board.place_stone(Player(Color.WHITE), Point(row=1, col=2))
        board.place_stone(Player(Color.BLACK), Point(row=1, col=3))
        board.place_stone(Player(Color.BLACK), Point(row=2, col=2))
#        board.place_stone(Player(Color.BLACK), Point(row=1, col=1))
        self.assertIsNone(board._grid.get(Point(row=1, col=2)))  # Stone should be captured
        self.assertIsNotNone(board._grid.get(Point(row=2,col=2))) # Stone should stay on the board


class TestGameState(unittest.TestCase):
    def test_new_game(self):
        game = GameState.new_game(19)
        self.assertEqual(game.board.num_rows, 19)
        self.assertEqual(game.board.num_cols, 19)
        self.assertEqual(game.next_player.color, Color.BLACK)
        self.assertIsNone(game.previous_state)
        self.assertIsNone(game.last_move)

    def test_apply_move(self):
        game = GameState.new_game(19)
        move = Move.play(Point(4, 5))
        game_after_move = game.apply_move(move)
        self.assertIsNot(game.board, game_after_move.board)
        self.assertIsNotNone(game_after_move.board._grid.get(Point(4, 5)))
        self.assertEqual(game_after_move.next_player.color, Color.WHITE)
        self.assertIs(game_after_move.previous_state, game)
        self.assertIs(game_after_move.last_move, move)

    def test_is_move_self_capture(self):
        game = GameState.new_game(19)
        game = game.apply_move(Move.play(Point(1, 2)))
        game = game.apply_move(Move.play(Point(1, 3)))
        game = game.apply_move(Move.play(Point(2, 1)))
        game = game.apply_move(Move.play(Point(2, 2)))
        game = game.apply_move(Move.play(Point(3, 2)))
        game = game.apply_move(Move.play(Point(3, 1)))
        self.assertTrue(game.is_move_self_capture(Player(Color.BLACK), Move.play(Point(1, 1))))

    def test_does_move_violate_ko(self):
        game = GameState.new_game(9)
        #game.board.place_stone(Player(Color.BLACK), Point(1, 1))
        #game.board.place_stone(Player(Color.WHITE), Point(2, 1))
        #game.board.place_stone(Player(Color.WHITE), Point(1, 2))
        game = game.apply_move(Move.play(Point(2, 1)))  #black
        game = game.apply_move(Move.play(Point(3, 1)))  #white
        game = game.apply_move(Move.play(Point(1, 2)))  #black
        game = game.apply_move(Move.play(Point(4, 2)))  #white
        game = game.apply_move(Move.play(Point(2, 3)))  #black
        game = game.apply_move(Move.play(Point(3, 3)))  #white
        game = game.apply_move(Move.play(Point(3, 2)))  #black
        game = game.apply_move(Move.play(Point(2, 2)))  #white
        self.assertIsNone(game.board._grid.get(Point(row=3, col=2)))  # Stone should be captured
        self.assertTrue(game.does_move_violate_ko(Player(Color.BLACK), Move.play(Point(3, 2))))
        game = game.apply_move(Move.play(Point(3, 2)))  #black
        self.assertIsNone(game.board._grid.get(Point(row=2, col=2)))  # Stone should be captured
        self.assertTrue(game.does_move_violate_ko(Player(Color.WHITE), Move.play(Point(2, 2))))


    def test_is_valid_move(self):
        game = GameState.new_game(19)
        self.assertTrue(game.is_valid_move(Move.play(Point(1, 2))))
        game = game.apply_move(Move.play(Point(1, 2))) #black
        self.assertFalse(game.is_valid_move(Move.play(Point(1, 2))))  # occupied point
        game = game.apply_move(Move.play(Point(1, 3))) #white
        game = game.apply_move(Move.play(Point(2, 1))) #black
        game = game.apply_move(Move.play(Point(2, 2))) #white
        game = game.apply_move(Move.play(Point(3, 2))) #black
        game = game.apply_move(Move.play(Point(3, 1))) #white      
      #  game.board.place_stone(Player(Color.WHITE), Point(2, 1)) #white
      #  game.board.place_stone(Player(Color.WHITE), Point(1, 2)) #black
        self.assertFalse(game.is_valid_move(Move.play(Point(1, 1))))  # self-capture

    def test_is_over(self):
        game = GameState.new_game(19)
        self.assertFalse(game.is_over())
        game = game.apply_move(Move.pass_turn())
        self.assertFalse(game.is_over())
        game = game.apply_move(Move.pass_turn())
        self.assertTrue(game.is_over())
        game = GameState.new_game(19).apply_move(Move.resign())
        self.assertTrue(game.is_over())
        

if __name__ == '__main__':
    unittest.main()
