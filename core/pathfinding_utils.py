from core.state import State
import heapq
import itertools

class PathfindingUtils:
    def __init__(self, grid):
        self.grid = grid
        self._tail_reach_cache = {}

    def tail_reachable(self, snake, bnb_path_func):
        """Check if snake's tail is reachable from its head using bnb_path_func"""
        if len(snake.body) <= 2:
            return True
        state = State(snake.head, tuple(snake.body), snake.body[-1])
        if state in self._tail_reach_cache:
            return self._tail_reach_cache[state]
        path = bnb_path_func(snake.head, snake.body[-1], snake.body[:-1])
        result = bool(path)
        self._tail_reach_cache[state] = result
        return result

    def astar_generator(self, snake, apple, batch_size=1):
        """A* generator for real-time visualization. Yields after each batch of node expansions."""
        visited = set()
        visited_heads = set()
        heap = []
        batch_count = 0
        total_expanded = 0
        counter = itertools.count()
        def heuristic(pos):
            return abs(pos.x - apple.x) + abs(pos.y - apple.y)
        start_snake = snake.copy()
        heapq.heappush(heap, (heuristic(start_snake.head), next(counter), 0, start_snake, []))
        found_path = None
        while heap:
            f_score, _, g_score, current_snake, path = heapq.heappop(heap)
            head = current_snake.head
            state_sig = (current_snake.head, tuple(current_snake.body))
            if state_sig in visited:
                continue
            visited.add(state_sig)
            if head not in visited_heads:
                visited_heads.add(head)
            if head == apple:
                new_snake = current_snake.copy()
                new_snake.grow()
                found_path = path
                yield (set(visited_heads), list(path), found_path)
                return
            for next_pos in head.neighbors():
                if not self.grid.is_inside(next_pos):
                    continue
                if next_pos in current_snake.body[:-1]:
                    continue
                new_snake = current_snake.copy()
                new_snake.move_towards(next_pos)
                new_path = path + [next_pos]
                new_state_sig = (new_snake.head, tuple(new_snake.body))
                if new_state_sig in visited:
                    continue
                h = heuristic(new_snake.head)
                heapq.heappush(heap, (g_score + 1 + h, next(counter), g_score + 1, new_snake, new_path))
            batch_count += 1
            total_expanded += 1
            dynamic_batch_size = min(1.15**100, max(1, 1 * 1.15**min(100,total_expanded) // 100))
            if batch_count >= dynamic_batch_size:
                yield (set(visited_heads), list(path), found_path)
                batch_count = 0
        yield (set(visited_heads), [], found_path)
