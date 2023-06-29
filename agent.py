from dataclasses import dataclass
from position import add_position
import random
import math
import time
import AStar
from vector import Vector
from parameters import *
from pre_render import prerender_characters

@add_position
@dataclass
class Agent:
    speed:float = 0.2
    last_step_time = 0
    x:int = 10
    y:int = 10
    px_x:int = px_to_grid(x)
    px_y:int = px_to_grid(y)

    color:str = "#33ddee"
    icon = "\ue11d"
    char = prerender_characters(icon, color)

    target:Vector = None
    path:list = None

    def set_color(self, color):
        self.color = color
        self.char = prerender_characters(self.icon, color)

    def seek():
        # takes an argument such as
        # food or resource
        pass

    def __set_px_coords__(self):
        self.px_x = px_to_grid(self.x)
        self.px_y = px_to_grid(self.y)

    def __set_grid_coords__(self):
        self.x = grid_to_px(self.px_x)
        self.y = grid_to_px(self.px_y)

    def update(self):
        if self.target:
            self.path = AStar.astar_pathfinding((self.x, self.y), self.target)
        if self.path:
            self.will_self()
        else:
            self.random_walk()

    def show(self, screen):
        self.__set_px_coords__()
        draw_object(self.char[0], screen, self.px_x, self.px_y)

    def random_walk(self):
        current_time = time.time()
        elapsed_time = current_time-self.last_step_time
        if elapsed_time >= self.speed:
            # Generate a random direction
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])

            # Update the agent's position
            self.x = self.x + dx
            self.y = self.y + dy
            print(f"agent: {self.x}, {self.y}")
            self.last_step_time = current_time

    def set_target(self, target):
        self.target = target

    def will_self(self):
        current_time = time.time()
        elapsed_time = current_time-self.last_step_time
        if elapsed_time >= self.speed:
            target = self.path[0]
            print(f"agent: {self.x}, {self.y}")

            self.x = target[0]
            self.y = target[1]
            self.path.pop(0)

            self.last_step_time = current_time