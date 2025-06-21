from dataclasses import dataclass

@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def neighbors(self):
        return [
            Position(self.x + 1, self.y),
            Position(self.x - 1, self.y),
            Position(self.x, self.y + 1),
            Position(self.x, self.y - 1)
        ]