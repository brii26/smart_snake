from core.pathfinder import Pathfinder
from core.state import State
from utils.position import Position

class SnakePlanner:
    def __init__(self, grid):
        self.grid = grid
        self.pathfinder = Pathfinder(grid)
        self.memo = set()

    def find_safe_path(self, snake, apple: Position):
        # Step 1: Try safe path (tail-reachable)
        path = self.pathfinder.a_star(snake.head, apple, snake.body)
        if path:
            simulated_snake = snake.copy()
            for move in path:
                simulated_snake.move_towards(move)
            simulated_snake.grow()

            if self.tail_reachable(simulated_snake):
                return path  # ✅ Safe path found

        # Step 2: Fallback - return path even if unsafe (better than dying)
        return path  # Might be unsafe but better than nothing


    def tail_reachable(self, snake):
        if len(snake.body) <= 2:
            return True  # too short to trap

        state = State(snake.head, tuple(snake.body), snake.body[-1])
        if state in self.memo:
            return False

        path = self.pathfinder.a_star(snake.head, snake.body[-1], snake.body)
        if path:
            return True

        self.memo.add(state)
        return False
