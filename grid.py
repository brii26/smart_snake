import random
from utils.position import Position

class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def is_inside(self, pos: Position) -> bool:
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def random_empty_position(self, snake) -> Position:
        all_positions = [Position(x, y) for x in range(self.width) for y in range(self.height)]
        free = [p for p in all_positions if p not in snake.body]
        return random.choice(free)

    def center_position(self) -> Position:
        return Position(self.width // 2, self.height // 2)