from dataclasses import dataclass
from utils.position import Position

@dataclass(frozen=True)
class State:
    head: Position
    body: tuple[Position, ...]  # full body including head
    apple: Position

    def is_valid(self, grid, ignore_tail=False) -> bool:
        # Check head inside grid
        if not grid.is_inside(self.head):
            return False

        # Check collision with body (optionally ignore tail)
        body_check = self.body[:-1] if ignore_tail else self.body
        return self.head not in body_check
