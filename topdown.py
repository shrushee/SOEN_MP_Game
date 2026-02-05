import pygame
from sys import exit
import math
from settings import *
import asyncio

pygame.init()

#Creating window
screen = pygame.display.set_mode((WIDTH), (HEIGHT))
pygame.display.set_caption("QHHS Map Test")
clock = pygame.time.Clock()

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()