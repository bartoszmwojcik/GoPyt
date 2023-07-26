# Filename: dlgo/zobrist.py

import random
from .gotypes import Color, Point

def init_zobrist(board_size):
    max_hashval = 1 << 64  # Use 64-bit hashes
    table = {}

    for row in range(1, board_size + 1):
        for col in range(1, board_size + 1):
            table[(Point(row, col), Color.BLACK)] = random.randint(0, max_hashval)
            table[(Point(row, col), Color.WHITE)] = random.randint(0, max_hashval)
    return table

def print_zobrist_table(table):
    for key, value in table.items():
        point, color = key
        print(f"Point: {point}, Color: {color}, Hash: {value}")

def update_hash(current_hash, color, point, zobrist_table):
    """
    Update the Zobrist hash of a board state.

    :param current_hash: the current hash
    :param color: the color of the stone being placed or removed
    :param point: the point where the stone is being placed or removed
    :param zobrist_table: the Zobrist hash table
    :return: the updated hash
    """
    return current_hash ^ zobrist_table[(point, color)]
