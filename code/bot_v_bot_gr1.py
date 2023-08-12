# Filename: dlgo/bot_v_bot_gr1.py

import pygame
import time
import sys
from dlgo import goboard
from dlgo import gotypes
from dlgo.utils import print_move
from dlgo.agent.naive import RandomBot, SafetyBot, MinimaxBot
from dlgo.agent.helpers import evaluate_safety_nuanced, evaluate_territory, evaluate_safety, evaluate_high_safety

# Pygame-specific settings
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (231,158,107)
GRID_SIZE = 5
SQUARE_SIZE = 80  # size of each square on the board
WIDTH = HEIGHT = SQUARE_SIZE * GRID_SIZE
STONE_RADIUS = SQUARE_SIZE * 0.4

# Create Pygame screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption ("Safety vs Safety Nuanced")
#pygame.display.set_caption ("Safety Nuanced vs Safety")
#pygame.display.set_caption ("Random vs Safety Nuanced")
#pygame.display.set_caption ("Random vs Safety")
#pygame.display.set_caption ("Random vs Territory")
#pygame.display.set_caption ("Random vs High Safety")
pygame.display.set_caption ("Safety Nuanced 3x vs Safety Nuanced")

game = None

while game is None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()        
        if event.type == pygame.KEYDOWN:
            # Create the Go board and bots
            game = goboard.GameState.new_game(GRID_SIZE)

bots = {
#    gotypes.Color.BLACK: RandomBot("black"),
#    gotypes.Color.BLACK: SafetyBot("black", evaluate_safety),
    gotypes.Color.BLACK: MinimaxBot("black", 3, evaluate_safety_nuanced),
#    gotypes.Color.WHITE: SafetyBot("white", evaluate_safety_nuanced), 
    gotypes.Color.WHITE: SafetyBot("white", evaluate_safety_nuanced), 
#    gotypes.Color.WHITE: SafetyBot("white", evaluate_safety), 
#    gotypes.Color.WHITE: SafetyBot("white", evaluate_territory), 
}

while game is not None:
    time.sleep (0.3)
    bot_move = bots[game.next_player.color].select_move(game)
    print_move(game.next_player, bot_move)
    game = game.apply_move(bot_move)

    # Draw the board
    screen.fill(ORANGE)
    for i in range(GRID_SIZE):
        pygame.draw.lines(screen, BLACK, False, [(i*SQUARE_SIZE + STONE_RADIUS, 0), (i*SQUARE_SIZE + STONE_RADIUS, HEIGHT)], 1)
        pygame.draw.lines(screen, BLACK, False, [(0, i*SQUARE_SIZE + STONE_RADIUS), (WIDTH, i*SQUARE_SIZE+ STONE_RADIUS)], 1)

    # Draw the stones
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            point = gotypes.Point(row + 1, col + 1)
            stone = game.board.get_color(point)
            if stone is not None:
                color = BLACK if stone == gotypes.Color.BLACK else WHITE
                pos = (col * SQUARE_SIZE + STONE_RADIUS, row * SQUARE_SIZE + STONE_RADIUS)
                pygame.draw.circle(screen, color, pos, STONE_RADIUS)

    pygame.display.update()

    # Exit if the game is over
    if game.is_over():
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = None

while game is not None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = None

pygame.quit()
