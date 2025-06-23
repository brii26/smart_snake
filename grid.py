import random
from utils.position import Position

class Grid:
    def __init__(self, width: int, height: int):
        """Initialize the grid with the given width and height."""
        self.width = width
        self.height = height

    def is_inside(self, pos: Position) -> bool:
        """Check if a position is inside the grid boundaries."""
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def random_empty_position(self, snake):
        """Return a random empty position not occupied by the snake."""
        available = [
            Position(x, y)
            for x in range(self.width)
            for y in range(self.height)
            if Position(x, y) not in snake.body
        ]
        return random.choice(available) if available else None

    def center_position(self) -> Position:
        """Return the center position of the grid."""
        return Position(self.width // 2, self.height // 2)