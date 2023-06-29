from dataclasses import dataclass
from position import add_position

@add_position
@dataclass
class Food:
    name: str
    amount: int
    energy: int

food = Food("carrot", 2, 4)
food.position = (2,4)

print(food.position)