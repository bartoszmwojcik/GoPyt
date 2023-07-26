# in utils.py

COLS = 'ABCDEFGHJKLMNOPQRST'

def print_move(player, move):
    """
    Prints a move in a human-readable format.
    """
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = '%s%d' % (COLS[move.point.col - 1], move.point.row)
    print('%s %s' % (player, move_str))
