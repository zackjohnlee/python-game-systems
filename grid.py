import math
from parameters import *

class Grid:
    def __init__(self, grid):
        self.nodes = []
        self.edges = {}
        self.costs = {}

        # Create a node for each point on the grid
        for row in range(grid_row):
            for col in range(grid_col):
                node = (row, col)
                self.nodes.append(node)

                # Add edges to neighboring nodes
                neighbors = self.get_neighbors(node)
                for neighbor in neighbors:
                    self.add_edge(node, neighbor)

    def add_edge(self, node1, node2):
        # Add an undirected edge between two nodes
        if node1 not in self.edges:
            self.edges[node1] = []
        if node2 not in self.edges:
            self.edges[node2] = []
        self.edges[node1].append(node2)
        self.edges[node2].append(node1)

        # Compute the cost of the edge as the Euclidean distance between the nodes
        cost = math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)
        self.costs[(node1, node2)] = cost
        self.costs[(node2, node1)] = cost

    def get_neighbors(self, node):
        # Get the neighboring nodes of a given node
        row, col = node
        neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1),
                     (row-1, col-1), (row+1, col-1), (row-1, col+1), (row+1, col+1)]
        neighbors = [n for n in neighbors if n in self.nodes]
        return neighbors

    def get_cost(self, node1, node2):
        # Get the cost of traveling from node1 to node2
        return self.costs[(node1, node2)]
