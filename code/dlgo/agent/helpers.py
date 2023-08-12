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

# Simple Territory Counting:
# The most straightforward way to evaluate a board is to count the number of stones and territories for each player.
def evaluate_territory(board):
    territory_count = {Color.BLACK: 0, Color.WHITE: 0}
    for row in range(1, board.num_rows + 1):
        for col in range(1, board.num_cols + 1):
            point = Point(row, col)
            owner = board.get_color(point)
            if owner is not None:
                territory_count[owner] += 1
    return territory_count

# Stone Safety Evaluation:
# Instead of just counting territories, consider how safe each stone or group of stones is. 
# A stone or a group that has only one or two liberties (spaces where a new stone could be placed) is in danger of being captured.
def evaluate_safety(board):
    score = {Color.BLACK: 0, Color.WHITE: 0}
    for _, group in board._grid.items():
        if group.num_liberties > 2:
            score[group.color] += len(group.stones)
        else:
            score[group.color] -= len(group.stones)  # penalize groups with 1 or 2 liberties
    return score

# Stone Safety Evaluation more nuanced
def evaluate_safety_nuanced(board):
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

# Stone Safety Evaluation even more nuanced
def evaluate_high_safety(board):
    score = {Color.BLACK: 0, Color.WHITE: 0}
        
    for _, group in board._grid.items():
        base_score = len(group.stones)
            
        # Modify the score based on the number of liberties.
        if group.num_liberties == 1:
            score[group.color] -= base_score  # heavy penalty for Atari
        elif group.num_liberties == 2:
            score[group.color] -= base_score * 0.5  # lighter penalty for potential danger
        else:
            score[group.color] += base_score * 0.5 # positive score for safe groups
        
        # Additionally, add a bonus for each liberty for groups with >2 liberties.
        if group.num_liberties > 2:
            score[group.color] += group.num_liberties  # for instance, half a point per liberty
      
    return score