import pygame
import random
import time
from parameters import *
import math
from heapq import heappop, heappush

def astar_pathfinding(start, target):
        # Heuristic function (Manhattan distance)
        def heuristic(position):
            return abs(target[0] - position[0]) + abs(target[1] - position[1])

        # Neighbors function (up, down, left, right)
        def neighbors(position):
            x, y = position
            neighbors = [(x, y - 1), (x, y + 1), 
                         (x - 1, y), (x + 1, y), 
                         (x + 1, y + 1), (x - 1, y - 1), 
                         (x + 1, y - 1), (x - 1, y + 1)]
            return [n for n in neighbors if 0 <= n[0] < grid_width and 0 <= n[1] < grid_height]

        # A* algorithm implementation
        open_list = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start)}

        while open_list:
            current_score, current_position = heappop(open_list)

            if current_position == target:
                # Reconstruct the path
                path = []
                while current_position in came_from:
                    path.append(current_position)
                    current_position = came_from[current_position]
                path.reverse()
                return path

            for neighbor in neighbors(current_position):
                g = g_score[current_position] + 1

                if neighbor not in g_score or g < g_score[neighbor]:
                    g_score[neighbor] = g
                    f = g + heuristic(neighbor)
                    f_score[neighbor] = f
                    heappush(open_list, (f, neighbor))
                    came_from[neighbor] = current_position

        return []  # No path found
