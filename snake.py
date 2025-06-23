from utils.position import Position

class Snake:
    def __init__(self, start: Position):
        self.body = [start, Position(start.x, start.y + 1)]
        self.last_direction = (0, -1)

    @property
    def head(self) -> Position:
        return self.body[0]

    def move_towards(self, next_pos: Position):
        dx = next_pos.x - self.head.x
        dy = next_pos.y - self.head.y
        if (dx != 0 or dy != 0) and next_pos != self.head:
            self.last_direction = (dx, dy)
        self.body.insert(0, next_pos)
        self.body.pop()

    def grow(self, direction=None):
        self.body.append(self.body[-1])
        if direction is not None:
            self.last_direction = direction
        elif len(self.body) > 1:
            dx = self.body[0].x - self.body[1].x
            dy = self.body[0].y - self.body[1].y
            self.last_direction = (dx, dy)

    def is_collision(self, pos: Position) -> bool:
        return pos in self.body

    def copy(self):
        clone = Snake(self.body[0])
        clone.body = self.body.copy()
        clone.last_direction = self.last_direction
        return clone