import pygame

grid_row = 35
grid_col = 50
cell_size = 20
spacing = 0

grid_width = grid_col * (cell_size + spacing) - spacing
grid_height = grid_row * (cell_size + spacing) - spacing


def px_to_grid(x):
    x = x * (cell_size + spacing)
    return x


def grid_to_px(x):
    x = x // (cell_size + spacing)
    return x


def draw_object(obj, surface, cell_x, cell_y):
    text_rect = obj.get_rect(
        center=(cell_x + cell_size // 2, cell_y + cell_size // 2))
    # print(text_rect, surface)
    surface.blit(obj, text_rect)
