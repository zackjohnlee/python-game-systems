import pygame
import pygame_gui
import random
from agent import Agent
from parameters import *
import pre_render
import AStar
import threading

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((grid_width, grid_height))

active_surface = pygame.Surface((grid_width, grid_height), pygame.SRCALPHA)
active_surface.fill((0,0,0,0))
grass_surface = pygame.Surface((grid_width, grid_height), pygame.SRCALPHA)
grass_surface.fill((0,0,0,0))
background = pygame.Surface((grid_width, grid_height))
background.fill(pygame.Color('#333333'))

manager = pygame_gui.UIManager((grid_width, grid_height))

grass_chars = ["\u2801", "\u2802", "\u2056", "\u205b", 
              "\u2808", "\u280a", "\u280c", "\u2810", 
              "\u2820", "\u2882", "\u288c", "\u2888",
              "\u2234", "\u2237"]
              
grid = [[None for _ in range(grid_width)] for _ in range(grid_height)]

# Function to generate objects randomly in the grid
def generate_objects(chars):
    for x in range(grid_col):
        for y in range(grid_row):
            # Randomly choose a grass character for each cell
            object_char = random.choice(chars)
            grid[y][x] = object_char

grass = pre_render.prerender_characters(grass_chars, (74, 152, 111))
agent_char = pre_render.prerender_characters("\u26c4", (255,255,255))
generate_objects(grass)

def update_grid():
    # Draw grid cells
    for row in range(grid_row):
        for col in range(grid_col):
            # Calculate the position of the cell
            x = col
            y = row

            obj_char = grid[y][x]
            if obj_char is not None:
                draw_object(obj_char, grass_surface, px_to_grid(x), px_to_grid(y))


agent_1 = Agent()
agent_2 = Agent(x=20, y=30, speed=0.42)
agent_2.set_color("#22ee99")

# def find_path(start_pos, end_pos):
#     # Perform A* pathfinding and return the path
#     graph = Graph(grid)
#     start = graph.get_node_at_pixel(*start_pos)
#     end = graph.get_node_at_pixel(*end_pos)
#     path = AStar.astar(graph, start, end)
#     return path

clock = pygame.time.Clock()
# pathfinding_thread = threading.Thread(target=find_path, args=(start_pos, end_pos))
# pathfinding_thread.start()
is_running = True
update_grid()

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            # pygame.quit()
            # SystemExit()

    # target = (0,0)

    # if pathfinding_thread.is_alive():
    #     # Pathfinding is still running, do nothing
    #     pass
    # else:
    #     # Pathfinding is complete, update the agent's path
    #     agent_1.path = pathfinding_thread.result
 

    if pygame.time.get_ticks() % 120 == 0:
        # start = (agent_1.x, agent_1.y)
        rand_a = random.randint(0, grid_width - 1)
        rand_b = random.randint(0, grid_height - 1)
        # target = (grid_to_px(rand_a), 
        #           grid_to_px(rand_b))
        # # target = (grid_to_px(400), grid_to_px(400))
        show_target = (rand_a, rand_b)
        background.fill("#333333")
        pygame.draw.circle(background, (255, 0, 0, 1), show_target, 10)
        # path = AStar.astar_pathfinding(start, target)
        # print(path)
        # agent_1.path = path
        agent_1.target = (grid_to_px(rand_a), 
                        grid_to_px(rand_b))

    agent_2.target = (agent_1.x, agent_1.y)
    active_surface.fill((0,0,0,0))
    agent_1.update()
    agent_1.show(active_surface)
    agent_2.update()
    agent_2.show(active_surface)


    # manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    window_surface.blit(grass_surface, (0, 0))
    window_surface.blit(active_surface, (0, 0))

    # manager.draw_ui(window_surface)
    clock.tick(30)

    pygame.display.update()

pygame.quit()