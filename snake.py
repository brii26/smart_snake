from utils.position import Position

class Snake:
    def __init__(self, start: Position):
        self.body = [start]  # head = body[0]

    @property
    def head(self) -> Position:
        return self.body[0]

    def move_towards(self, next_pos: Position):
        self.body.insert(0, next_pos)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])  # duplicate last tail segment

    def is_collision(self, pos: Position) -> bool:
        return pos in self.body

    def copy(self):
        clone = Snake(self.body[0])
        clone.body = self.body.copy()
        return clone