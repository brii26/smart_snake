import random
from utils.position import Position

class Grid:
    def __init__(self, width: int, height: int):
        """Initialize grid"""
        self.width = width
        self.height = height

    def is_inside(self, pos: Position) -> bool:
        """cell is inside the grid validation"""
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def random_empty_position(self, snake):
        """Return random empty cell"""
        available = [
            Position(x, y)
            for x in range(self.width)
            for y in range(self.height)
            if Position(x, y) not in snake.body
        ]
        return random.choice(available) if available else None

    def center_position(self) -> Position:
        """Return center grid position"""
        return Position(self.width // 2, self.height // 2)