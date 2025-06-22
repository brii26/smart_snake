from core.pathfinder import Pathfinder
from core.state import State
from utils.position import Position
from collections import deque

class SnakePlanner:
    def __init__(self, grid):
        self.grid = grid
        self.pathfinder = Pathfinder(grid)
        self.memo = set()

    def find_safe_path(self, snake, apple: Position):
        visited = set()
        queue = deque()
        fallback_path = None  # Will store first apple-reaching path even if unsafe
        queue.append((snake.copy(), []))  # (snake_state, path)

        while queue:
            current_snake, path = queue.popleft()
            head = current_snake.head

            if head == apple:
                new_snake = current_snake.copy()
                new_snake.grow()
                if self.tail_reachable(new_snake):
                    print(f"[DEBUG] ✅ Found safe path to apple (length {len(path)})")
                    return path
                elif fallback_path is None:
                    print(f"[DEBUG] ⚠ Apple reached, but tail NOT reachable — saving fallback path")
                    fallback_path = path
                continue

            for next_pos in head.neighbors():
                if not self.grid.is_inside(next_pos):
                    continue
                if next_pos in current_snake.body[:-1]:  # tail ignored
                    continue

                new_snake = current_snake.copy()
                new_snake.move_towards(next_pos)
                new_path = path + [next_pos]

                state_sig = (new_snake.head, tuple(new_snake.body))
                if state_sig in visited:
                    continue
                visited.add(state_sig)
                queue.append((new_snake, new_path))

        if fallback_path:
            print("[DEBUG] ❌ No safe path, returning fallback (unsafe) path")
            return fallback_path

        print("[DEBUG] ❌ No path to apple at all")
        return None


    def tail_reachable(self, snake):
        if len(snake.body) <= 2:
            return True

        state = State(snake.head, tuple(snake.body), snake.body[-1])
        if state in self.memo:
            return False

        # Exclude tail from obstacle, as it moves away
        path = self.pathfinder.bnb_path(snake.head, snake.body[-1], snake.body[:-1])
        if path:
            return True

        self.memo.add(state)
        return False

