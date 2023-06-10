import Constants
import os
import pygame

pygame.init()

# Font Sizes
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 45)
largefont = pygame.font.SysFont("comicsansms", 65)

# Initialization of pitch
pitch_image = pygame.image.load(os.path.join('Assets', 'pitch.jpg'))
pitch = pygame.transform.scale(pitch_image, (Constants.WIDTH, Constants.HEIGHT))

# Initialization of player 1
poland_image = pygame.image.load(os.path.join('Assets', 'polishteam.png'))
poland = pygame.transform.scale(poland_image, (Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT))

# Initialization of player 2
germany_image = pygame.image.load(os.path.join('Assets', 'gremanteam.png'))
germany = pygame.transform.scale(germany_image, (Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT))

# Initialization of ball
ball_image = pygame.image.load(os.path.join('Assets', 'Ball.png'))
ball = pygame.transform.scale(ball_image, (Constants.BALL_WIDTH, Constants.BALL_WIDTH))

# Initialization of window
win = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
pygame.display.set_caption("Soccer Game")

white = (255, 255, 255)

grey = (169, 169, 169)
