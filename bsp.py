import random
import pprint
import rustworkx as rx
import numpy
import itertools as iter

class Room:
    def __init__(self, x, y, width, height):
        self.pos = (x, y)
        self.dim = (width, height)
        

    def __repr__(self):
        rep = f"({self.pos}, {self.dim})"
        return rep

class Structure:
    def __init__(self, width, height, room_count):
        self.width = width
        self.height = height
        self.room_count = room_count
        self.grid = [[0] * self.height for _ in range(self.width)]
        self.space_graph = rx.PyGraph(multigraph=False)
        self.walls = []
        self.rooms = []

    def structure_grid(self):
        self.grid =  [[0] * self.height for _ in range(self.width)]

    def bsp_grid(self, grid, room_count, offset_x=0, offset_y=0):

        height = len(grid)
        width = len(grid[0])

        split_count = room_count - 1
        split_width = random.randint(width // 3.5, width - 2) if width >= 3 else width // 2
        split_height = random.randint(height // 3.5, height - 2) if height >= 3 else height // 2

        left =  []
        right = []

        left_x = offset_x
        left_y = offset_y
        left_size = (split_width, height)

        right_x = offset_x + split_width + 1
        right_y = offset_y
        right_size = (width - split_width - 1, height)

        top_x = offset_x
        top_y = offset_y
        top_size = (width, split_height)

        bottom_x = offset_x
        bottom_y = offset_y + split_height + 1
        bottom_size = (width, height - split_height - 1)

        # Base Case
        if split_count <= 0:

            if width >= height: # vertical split
                for i in range(height):
                    self.grid[i + offset_y][split_width + offset_x] = 4
                self.rooms.append(Room(left_x, left_y, left_size[0], left_size[1]))
                self.rooms.append(Room(right_x, right_y, right_size[0], right_size[1]))
                
            else:
                for i in range(width):
                    self.grid[offset_y + split_height][i + offset_x] = 4
                self.rooms.append(Room(top_x, top_y, top_size[0], top_size[1]))
                self.rooms.append(Room(bottom_x, bottom_y, bottom_size[0], bottom_size[1]))
            return

        # Recurssion
        if width >= height: # vertical split

            for i in range(height):
                self.grid[i + offset_y][split_width + offset_x] = split_count
                
                left.append([(x + left_x, i) for x in range(left_size[0])])
                right.append([(x + right_x, i) for x in range(right_size[0])])

            if len(left[0]) > len(right[0]):
                self.bsp_grid(left, split_count, offset_x, offset_y)
                self.bsp_grid(right, 1, offset_x + split_width + 1, offset_y)
            else:
                self.bsp_grid(right, split_count, offset_x + split_width + 1, offset_y)
                self.bsp_grid(left, 1, offset_x, offset_y)

        else: # horizontal split

            for i in range(width):
                self.grid[offset_y + split_height][i + offset_x] = split_count

                left.append([(i + offset_x, y + top_y) for y in range(top_size[1])])
                right.append([(i + offset_x, y + bottom_y) for y in range(bottom_size[1])])            

            # these 2 lines transpose the above matrices so they resemble the grid
            left = [[left[j][i] for j in range(len(left))] for i in range(len(left[0]))]
            right = [[right[j][i] for j in range(len(right))] for i in range(len(right[0]))]
            
            if len(left) > len(right):
                self.bsp_grid(left, split_count, offset_x, offset_y)
                self.bsp_grid(right, 1, offset_x, offset_y + split_height + 1)
            else:
                self.bsp_grid(right, split_count, offset_x, offset_y + split_height + 1)
                self.bsp_grid(left, 1, offset_x, offset_y)

    def build_space_graph(self):
        
        # sort the rooms by distance from (0,0)
        self.rooms.sort(key=lambda x: sum(x*x for x in x.pos))

        # grab the graph from self and intialize a node for each room
        space_graph = self.space_graph
        space_graph.add_nodes_from([(i.pos, i.dim) for i in self.rooms])
        
        min_max = []

        # finds the min/max values for each axis in each room
        for i, obj in enumerate(self.rooms):
            min_x = obj.pos[0] - 1
            max_x = obj.pos[0] + obj.dim[0]

            min_y = obj.pos[1] - 1
            max_y = obj.pos[1] + obj.dim[1]

            min_max.append([(min_x, max_x), (min_y, max_y), i])

        # pprint.pprint(min_max)
        
        room_combinations = list(iter.combinations(min_max, 2))
        # pprint.pprint(room_combinations)

        # for loop iterates over combinations and adds edges
        for i in room_combinations:
            a_x, a_y, a_index = i[0]
            b_x, b_y, b_index = i[1]

            a_max_x = a_x[1]
            a_min_x = a_x[0]
            b_max_x = b_x[1]
            b_min_x = b_x[0]

            a_max_y = a_y[1]
            a_min_y = a_y[0]
            b_max_y = b_y[1]
            b_min_y = b_y[0]

            # this checks if the 2 inputs are overlapping
            if b_min_x <= a_max_x and b_max_x >= a_min_x and b_min_y <= a_max_y and b_max_y >= a_min_y:

                # this chunk looks over the x and y axis and determine which walls are overlapping
                # uses list comprehension and checks if the min and max in a are overlapping the min and max in b
                x_overlap = [x for x in list(iter.chain(range(a_min_x, a_max_x+1))) if x in list(iter.chain(range(b_min_x, b_max_x+1)))]
                y_overlap = [y for y in list(iter.chain(range(a_min_y, a_max_y+1))) if y in list(iter.chain(range(b_min_y, b_max_y+1)))]
                wall_coords = list(iter.product(x_overlap, y_overlap))

                # so long as at least 3 walls are overlapping, add an edge between those nodes
                if len(wall_coords) >= 3:
                    space_graph.add_edge(a_index, b_index, wall_coords)
                    self.walls.append(wall_coords)

                    # print the node data along with its index, print the edge objects
                    # print(f"nodes linked: {a_index, space_graph.get_node_data(a_index)} <--> {b_index, space_graph.get_node_data(b_index)}")
                    # print(f"edge data: {(space_graph.get_all_edge_data(a_index, b_index))}")
        
        pprint.pprint(self.walls)
        print(f"edge list: {list(space_graph.edge_list())}")
        current_room_size = 0
        largest_room_index = 0
        for node in space_graph.node_indices():
            current_node = space_graph.get_node_data(node)
            next_room_size = current_node[1][0] * current_node[1][1]
            if next_room_size > current_room_size:
                current_room_size = next_room_size
                largest_room_index = node
        print(f"largest room: {space_graph.get_node_data(largest_room_index)} // {current_room_size} cells")
        print(f"larget room neighbors: {list(space_graph.neighbors(largest_room_index))}")        
    
    def generate_structure(self):
        self.bsp_grid(self.grid, self.room_count)
        self.build_space_graph()


grid = Structure(10,10, 4)
grid.generate_structure()
pprint.pprint(grid.grid)
# pprint.pprint(grid.rooms)
# pprint.pprint(grid.rooms[2].pos)
