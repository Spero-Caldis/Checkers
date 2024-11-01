import pygame

WIDTH,HEIGHT = 800,800
ROWS,COLS = 8,8
SQUARE_SIZE = WIDTH//COLS

#RGB
PLAYER_1 = (255,0,0)
PLAYER_2 = (0, 255, 0)
SQUARE_2 = (255,255,255)
SQUARE_1 = (0,0,0)
VALID = (0,0,255)
BORDER = (128, 128, 128)
CROWN = pygame.transform.scale(pygame.image.load('checkers/assets/crown.png'), (44,25))
