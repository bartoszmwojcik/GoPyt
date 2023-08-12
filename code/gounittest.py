# Filename: gounittest.py

import unittest
from dlgo.gotypes import Color, Player, Point, Move
from dlgo.goboard1 import Board, GameState
import dlgo.goboard as goboard
from dlgo.agent.helpers import is_eye, evaluate_safety_nuanced
from dlgo.agent.naive import RandomBot, SafetyBot
from dlgo.zobrist import init_zobrist, update_hash

class TestBoard1(unittest.TestCase):
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

class TestBoard(unittest.TestCase):
    def test_initialization(self):
        board = goboard.Board(num_rows=19, num_cols=19)
        self.assertEqual(board._grid, {})  # Board should start empty

    def test_place_stone(self):
        board = goboard.Board(num_rows=19, num_cols=19)
        board.place_stone(Player(Color.BLACK), Point(row=1, col=1))
        self.assertIsNotNone(board._grid.get(Point(row=1, col=1)))  # Stone should be placed

    def test_capture(self):
        board = goboard.Board(num_rows=19, num_cols=19)
        board.place_stone(Player(Color.BLACK), Point(row=1, col=1))
        board.place_stone(Player(Color.WHITE), Point(row=1, col=2))
        board.place_stone(Player(Color.BLACK), Point(row=1, col=3))
        board.place_stone(Player(Color.BLACK), Point(row=2, col=2))
#        board.place_stone(Player(Color.BLACK), Point(row=1, col=1))
        self.assertIsNone(board._grid.get(Point(row=1, col=2)))  # Stone should be captured
        self.assertIsNotNone(board._grid.get(Point(row=2,col=2))) # Stone should stay on the board

class TestGameState1(unittest.TestCase):
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
        
class TestGameState(unittest.TestCase):
    def test_new_game(self):
        game = goboard.GameState.new_game(19)
        self.assertEqual(game.board.num_rows, 19)
        self.assertEqual(game.board.num_cols, 19)
        self.assertEqual(game.next_player.color, Color.BLACK)
        self.assertIsNone(game.previous_state)
        self.assertIsNone(game.last_move)

    def test_apply_move(self):
        game = goboard.GameState.new_game(19)
        move = Move.play(Point(4, 5))
        game_after_move = game.apply_move(move)
        self.assertIsNot(game.board, game_after_move.board)
        self.assertIsNotNone(game_after_move.board._grid.get(Point(4, 5)))
        self.assertEqual(game_after_move.next_player.color, Color.WHITE)
        self.assertIs(game_after_move.previous_state, game)
        self.assertIs(game_after_move.last_move, move)

    def test_is_move_self_capture(self):
        game = goboard.GameState.new_game(19)
        game = game.apply_move(Move.play(Point(1, 2)))
        game = game.apply_move(Move.play(Point(1, 3)))
        game = game.apply_move(Move.play(Point(2, 1)))
        game = game.apply_move(Move.play(Point(2, 2)))
        game = game.apply_move(Move.play(Point(3, 2)))
        game = game.apply_move(Move.play(Point(3, 1)))
        self.assertTrue(game.is_move_self_capture(Player(Color.BLACK), Move.play(Point(1, 1))))

    def test_does_move_violate_ko(self):
        game = goboard.GameState.new_game(9)
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
        game = goboard.GameState.new_game(19)
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
        game = goboard.GameState.new_game(19)
        self.assertFalse(game.is_over())
        game = game.apply_move(Move.pass_turn())
        self.assertFalse(game.is_over())
        game = game.apply_move(Move.pass_turn())
        self.assertTrue(game.is_over())
        game = goboard.GameState.new_game(19).apply_move(Move.resign())
        self.assertTrue(game.is_over())

class TestIsEye(unittest.TestCase):
    def test_is_eye(self):
        board = Board(num_rows=19, num_cols=19)
        # place some stones on the board
        board.place_stone(Player(Color.BLACK), Point(row=1, col=1))
        board.place_stone(Player(Color.BLACK), Point(row=1, col=2))
        board.place_stone(Player(Color.BLACK), Point(row=2, col=1))
        board.place_stone(Player(Color.BLACK), Point(row=2, col=3))
        board.place_stone(Player(Color.BLACK), Point(row=3, col=2))
        board.place_stone(Player(Color.BLACK), Point(row=3, col=1))
        board.place_stone(Player(Color.BLACK), Point(row=3, col=3))
        # middle of the board
        self.assertTrue(is_eye(board, Point(row=2, col=2), Color.BLACK))  # Should be an eye.
        self.assertFalse(is_eye(board, Point(row=2, col=2), Color.WHITE))  # Should not be an eye for WHITE.

        # corner of the board
        board = Board(num_rows=19, num_cols=19)
        board.place_stone(Player(Color.BLACK), Point(row=2, col=2))
        board.place_stone(Player(Color.BLACK), Point(row=2, col=1))
        board.place_stone(Player(Color.BLACK), Point(row=1, col=2))
        self.assertTrue(is_eye(board, Point(row=1, col=1), Color.BLACK))  # Should be an eye.
        self.assertFalse(is_eye(board, Point(row=1, col=1), Color.WHITE))  # Should not be an eye for WHITE.

        # edge of the board
        board = Board(num_rows=19, num_cols=19)
        board.place_stone(Player(Color.BLACK), Point(row=2, col=2))
        board.place_stone(Player(Color.BLACK), Point(row=2, col=1))
        board.place_stone(Player(Color.BLACK), Point(row=3, col=2))
        board.place_stone(Player(Color.BLACK), Point(row=4, col=1))
        board.place_stone(Player(Color.BLACK), Point(row=4, col=2))      
        self.assertTrue(is_eye(board, Point(row=3, col=1), Color.BLACK))  # Should be an eye.
        self.assertFalse(is_eye(board, Point(row=3, col=1), Color.WHITE))  # Should not be an eye for WHITE.
        self.assertFalse(is_eye(board, Point(row=5, col=1), Color.BLACK))  # Should not be an eye.

class TestRandomBot(unittest.TestCase):

    def test_select_move(self):
        #board = Board(19)
        game = GameState.new_game(9)
        bot = RandomBot("naive")
        move = bot.select_move(game)
        self.assertTrue(game.is_valid_move(move))  # selected move should be valid
        
        game = game.apply_move(move)
        move = bot.select_move(game)
        self.assertTrue(game.is_valid_move(move))  # selected move should be valid

        game = game.apply_move(move)
        move = bot.select_move(game)
        self.assertTrue(game.is_valid_move(move))  # selected move should be valid

        #game.board.print_board()
        
class TestZobristHashing(unittest.TestCase):
    # ...
    def test_place_and_remove(self):
        zobrist_table = init_zobrist(19)
        initial_hash = 0

        for row_a in range(1, 20):
            for col_a in range(1, 20):
                point_a = Point(row=row_a, col=col_a)

                # Place a black stone and update the hash.
                hash_a = update_hash(initial_hash, Color.BLACK, point_a, zobrist_table)

                for row_b in range(1, 20):
                    for col_b in range(1, 20):
                        point_b = Point(row=row_b, col=col_b)

                        if point_a != point_b:
                            # Place a white stone and update the hash.
                            current_hash = update_hash(hash_a, Color.WHITE, point_b, zobrist_table)

                            # Remove the black stone and update the hash.
                            current_hash = update_hash(current_hash, Color.BLACK, point_a, zobrist_table)

                            # Remove the white stone and update the hash.
                            current_hash = update_hash(current_hash, Color.WHITE, point_b, zobrist_table)

                            # Check that the hash is the same as before.
                            self.assertEqual(current_hash, initial_hash)

class TestSafetyBot(unittest.TestCase):

    def test_select_move(self):
        #board = Board(19)
        game = GameState.new_game(9)
        bot = SafetyBot("SafetyBot", evaluate_safety_nuanced)
        move = bot.select_move(game)
        self.assertTrue(game.is_valid_move(move))  # selected move should be valid
        
        game = game.apply_move(move)
        move = bot.select_move(game)
        self.assertTrue(game.is_valid_move(move))  # selected move should be valid

        game = game.apply_move(move)
        move = bot.select_move(game)
        self.assertTrue(game.is_valid_move(move))  # selected move should be valid

if __name__ == '__main__':
    unittest.main()
