from core.pathfinder import Pathfinder
from core.state import State
from utils.position import Position
from collections import deque

class SnakePlanner:
    def __init__(self, grid):
        """Initialize the snake planner with the given grid."""
        self.grid = grid
        self.pathfinder = Pathfinder(grid)
        self.memo = set()
        self.visual_bfs_order = [] 

    def find_safe_path(self, snake, apple: Position):
        """Find a safe path from the snake to the apple using BFS."""
        visited = set()
        queue = deque()
        fallback_path = None
        self.visual_bfs_order = [] 
        queue.append((snake.copy(), []))

        while queue:
            current_snake, path = queue.popleft()
            head = current_snake.head

            if head not in self.visual_bfs_order:
                self.visual_bfs_order.append(head)

            if head == apple:
                new_snake = current_snake.copy()
                new_snake.grow()
                if self.tail_reachable(new_snake):
                    return path
                elif fallback_path is None:
                    fallback_path = path
                continue

            for next_pos in head.neighbors():
                if not self.grid.is_inside(next_pos):
                    continue
                if next_pos in current_snake.body[:-1]:
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
            return fallback_path
        
        return None

    def tail_reachable(self, snake):
        """Check if the snake's tail is reachable."""
        if len(snake.body) <= 2:
            return True

        state = State(snake.head, tuple(snake.body), snake.body[-1])
        if state in self.memo:
            return False

        # Exclude tail from obstacle
        path = self.pathfinder.bnb_path(snake.head, snake.body[-1], snake.body[:-1])
        if path:
            return True

        self.memo.add(state)
        return False

