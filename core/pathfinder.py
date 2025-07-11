from utils.position import Position
import heapq
import itertools

class Pathfinder:
    def __init__(self, grid):
        self.grid = grid
        self._tail_reach_cache = {}

    def bnb_path(self, start: Position, goal: Position, body: list[Position]) -> list[Position] | None:
        """Check if the tail is reachable (safe state)"""
        occupied = set(body[:-1])
        visited = set()

        def dfs(current, current_path):
            if current == goal:
                return current_path[:]

            visited.add(current)

            for next_pos in current.neighbors():
                if (not self.grid.is_inside(next_pos) or
                    next_pos in occupied or
                    next_pos in visited):
                    continue

                result = dfs(next_pos, current_path + [next_pos])
                if result:
                    return result

            return None

        return dfs(start, [])

    def astar_path(self, snake, apple: Position):
        """find a path from the snake's head to the apple. Returns path and visited nodes"""
        visited = set()
        visited_heads = set()
        heap = []
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
                return found_path, set(visited_heads)
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
        return None, set()
