from utils.position import Position

class Snake:
    def __init__(self, start: Position):
        """Initialize the snake with a head and one body segment behind it."""
        self.body = [start, Position(start.x, start.y + 1)]
        self.last_direction = (0, -1)

    @property
    def head(self) -> Position:
        """Return the current position of the snake's head."""
        return self.body[0]

    def move_towards(self, next_pos: Position):
        """Move the snake's head to the next position and update the body."""
        dx = next_pos.x - self.head.x
        dy = next_pos.y - self.head.y
        if (dx != 0 or dy != 0) and next_pos != self.head:
            self.last_direction = (dx, dy)
        self.body.insert(0, next_pos)
        self.body.pop()

    def grow(self, direction=None):
        """Grow the snake by duplicating the last tail segment."""
        self.body.append(self.body[-1])
        if direction is not None:
            self.last_direction = direction
        elif len(self.body) > 1:
            dx = self.body[0].x - self.body[1].x
            dy = self.body[0].y - self.body[1].y
            self.last_direction = (dx, dy)

    def is_collision(self, pos: Position) -> bool:
        """Check if the given position collides with any part of the snake's body."""
        return pos in self.body

    def copy(self):
        """Create a deep copy of the snake object, including its body and direction."""
        clone = Snake(self.body[0])
        clone.body = self.body.copy()
        clone.last_direction = self.last_direction
        return clone