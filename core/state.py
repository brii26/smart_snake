from dataclasses import dataclass
from utils.position import Position

@dataclass(frozen=True)
class State:
    head: Position
    body: tuple[Position, ...]  # head + body
    apple: Position

    def is_valid(self, grid, ignore_tail=False) -> bool:
        if not grid.is_inside(self.head):
            return False

        body_check = self.body[:-1] if ignore_tail else self.body
        return self.head not in body_check
