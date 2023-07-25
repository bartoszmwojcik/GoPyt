# Filename: goboard1.py
from gotypes import Point, Player, GoString, Color
import copy

COLS = 'ABCDEFGHJKLMNOPQERT'
STONE_TO_CHAR = {
    None: ' . ',
    Color.BLACK: ' x ', 
    Color.WHITE: ' o ',
}

class Board:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}
    def place_stone(self, player, point):
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        for neighbor in point.neighbors():  # assuming neighbors() method in Point class
            if not self.is_on_grid(neighbor):
                continue
            neighbor_string = self._grid.get(neighbor)
            if neighbor_string is None:
                liberties.append(neighbor)
            elif neighbor_string.color == player.color:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)
        new_string = GoString(player.color, [point], liberties)

        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        for new_point in new_string.stones:
            self._grid[new_point] = new_string

        for other_color_string in adjacent_opposite_color:
            other_color_string.remove_liberty(point)
        self._remove_dead_strings(adjacent_opposite_color, player)


    def is_on_grid(self, point):
        return 1 <= point.row <= self.num_rows and 1 <= point.col <= self.num_cols

    def _remove_dead_strings(self, strings, player):
        for string in strings:
            if string.num_liberties == 0:
                self._remove_string(string)

    def _remove_string(self, string):
        for point in string.stones:
            for neighbor in point.neighbors():  # assuming neighbors() method in Point class
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string.color == string.color:
                    continue
                if neighbor_string is not string:
                    neighbor_string.add_liberty(point)
            del(self._grid[point])
            #self._grid[point] = None

    def print_board (self):
        for row in range (self.num_rows, 0, -1):
            bump = " " if row <= 0 else ""
            line = []
            for col in range (1, self.num_cols + 1):
                stone = self.get_color (Point (row=row, col=col))
                line.append (STONE_TO_CHAR[stone])
            print ('%s%d %s' % (bump, row, ''.join(line)))
        print ('    ' + '  '.join(COLS[:self.num_cols]))

    def get_color(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color
    
    #def are_grids_eq (self, other):
    #    res = True
    #    for row in range (1, self.num_rows):
    #        for col in range (1, self.num_cols):
    #            stone_self = self._grid.get[Point(row=row, col=col)]  
    #            stone_other = other._grid.get[Point(row=row, col=col)]
    #            res = res and stone_self == stone_other
    #    return res
    
    def __eq__(self, other):
        return isinstance(other, Board) and \
            self.num_cols == other.num_cols and \
            self.num_rows == other.num_rows and \
            self._grid == other._grid
            #self.are_grids_eq (other)  


class GameState:
    def __init__(self, board, next_player, previous_state, last_move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous_state
        self.last_move = last_move

    def apply_move(self, move):
        """Return the new GameState after applying the move."""
        if move.is_play:
            new_board = copy.deepcopy(self.board)
            new_board.place_stone(self.next_player, move.point)
        else:
            new_board = self.board
        return GameState(new_board, self.next_player.other, self, move)

    @classmethod
    def new_game(cls, board_size):
        """Start a new game."""
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player(Color.BLACK), None, None)

    def is_move_self_capture(self, player, move):
        """Check if the given move is a self-capture."""
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)        
        next_board.place_stone(player, move.point)
        new_string = next_board._grid.get(move.point)    #get_go_string(move.point)
        return new_string.num_liberties == 0

    @property
    def situation(self):
        """Return the current situation (as a hashable)."""
        return (self.next_player, self.board)

    def does_move_violate_ko(self, player, move):
        """Check if a given move violates the Ko rule."""
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board)
        past_state = self.previous_state
        while past_state is not None:
            if past_state.situation == next_situation:
                return True
            past_state = past_state.previous_state
        return False

    def is_valid_move(self, move):
        """Determine if a move can be played in the current game state."""
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        return (
            self.board._grid.get(move.point) is None and
            not self.is_move_self_capture(self.next_player, move) and
            not self.does_move_violate_ko(self.next_player, move)
        )

    def is_over(self):
        """Check if the game is over."""
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass

 