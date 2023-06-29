import random
import pprint

class StructureGenerator:
    def __init__(self):
        self.grid = []
        self.walls = []
        self.rooms = []
    
    def split(self, grid, walls, room_count, offset_x=0, offset_y=0):
        
        height = len(grid)
        width = len(grid[0])

        if room_count <= 1:
            self.rooms.append(grid)
            
            if width >= height: # vertical split
                split_index = random.randint(1, width - 1)
                
                for i in range(height):
                    self.grid[i+offset_y][split_index + offset_x] = 2

            else:  # horizontal split
                split_index = random.randint(1, height - 1)
                
                for i in range(width):
                    self.grid[split_index+offset_y][i + offset_x] = 2

            return
        
        portion1 = []
        portion2 = []

        if width >= height: # vertical split
            split_index = random.randint(2, width - 3)
            
            for i in range(height):
                self.grid[i+offset_y][split_index + offset_x] = room_count - 1
                walls.append((i+offset_y, split_index + offset_x))
                portion1.append(grid[i][split_index + 1:])
                portion2.append(grid[i][:split_index])

            if len(portion1[0]) >= len(portion2[0]):
                self.rooms.append(portion2)
                self.split(portion1, walls, room_count - 1, offset_x + split_index + 1, offset_y)
                self.split(portion2, walls, 1, offset_x, offset_y)
            else:
                self.rooms.append(portion1)
                self.split(portion2, walls, room_count - 1, offset_x, offset_y)
                self.split(portion1, walls, 1, offset_x + split_index + 1, offset_y)

        else:  # horizontal split
            split_index = random.randint(2, height - 3)
            
            for i in range(width):
                self.grid[split_index+offset_y][i + offset_x] = room_count - 1 
                walls.append((split_index+offset_y, i + offset_x))

            for i in range(height):
                if i < split_index:
                    portion1.append(grid[i])
                elif i > split_index:
                    portion2.append(grid[i])

            if len(portion1) >= len(portion2):
                self.rooms.append(portion2)
                self.split(portion1, walls, room_count - 1, offset_x, offset_y)
                self.split(portion2, walls, 1, offset_x, offset_y + split_index + 1)
            else:
                self.rooms.append(portion1)
                self.split(portion2, walls, room_count - 1, offset_x, offset_y + split_index + 1)
                self.split(portion1, walls, 1, offset_x, offset_y)

    def generate_structure(self, size, room_count):
        self.grid = [[0] * size[1] for _ in range(size[0])]
        self.walls = []

        self.split(self.grid, self.walls, room_count)

        return self.grid, self.walls

# Example usage
size = (10,10)
room_count = 4

generator = StructureGenerator()
grid, walls = generator.generate_structure(size, room_count)

pprint.pprint(generator.rooms)
pprint.pprint(grid)
# pprint.pprint(walls)






