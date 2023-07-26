# Filename: helpers.py
from ..gotypes import Point, Color, Move

def is_eye(board, point, color):
    if board._grid.get(point) is not None:
        return False
    # All adjacent points must contain friendly stones.
    for neighbor in point.neighbors(): 
        if board.is_on_grid(neighbor):
            neighbor_color = board.get_color(neighbor)
            if neighbor_color != color:
                return False
    # We must control 3 out of 4 corners if the point is in the middle
    # of the board; on the edge you must control all corners
    friendly_corners = 0
    off_board_corners = 0
    corners = [
        Point(point.row - 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
        Point(point.row + 1, point.col + 1),
    ]
    for corner in corners:
        if board.is_on_grid(corner):
            corner_color = board.get_color(corner)
            if corner_color == color:
                friendly_corners += 1
        else:
            off_board_corners += 1
    if off_board_corners > 0:
        # Point is on the edge or corner.
        return off_board_corners + friendly_corners == 4
    # Point is in the middle.
    return friendly_corners >= 3

def legal_moves(game_state):
    moves = []
    for row in range(1, game_state.board.num_rows + 1):
        for col in range(1, game_state.board.num_cols + 1):
            move = Move.play(Point(row, col))
            if game_state.is_valid_move(move) and \
                not is_eye(game_state.board, Point(row, col), game_state.next_player.color):
                moves.append(move)
    # Include pass and resign for completeness
    if not moves:
        moves.append(Move.pass_turn())

    return moves
