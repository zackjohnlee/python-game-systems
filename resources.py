from dataclasses import dataclass
from position import add_position

# Resource Class
@add_position
@dataclass
class Resource:
    name: str
    amount: int
    weight: int

# Decorator
def processable_Decorator(resource_class):
    def wrapper(*args, **kwargs):
        obj = resource_class(*args, **kwargs)
        obj.process = lambda: print(f"Processing with {obj.name} material.")
        return obj
    return wrapper

# Factory
def Resource_Factory(name, amount, weight, processable=False):
    resource_class = Resource
    if processable:
        resource_class = processable_Decorator(resource_class)
    return resource_class(name, amount, weight)

resource_list = []
wood = Resource_Factory("wood", 20, 10, processable=True)
wood.process()