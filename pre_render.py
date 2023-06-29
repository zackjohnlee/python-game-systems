import pygame
from parameters import *

pygame.font.init()
font = pygame.font.SysFont("segoeuisymbol", cell_size)  # You can adjust the font size as needed

def prerender_characters(chars, color):
    rendered_chars = []
    for char in chars:
        text = font.render(char, True, color)
        rendered_chars.append(text)
    return rendered_chars