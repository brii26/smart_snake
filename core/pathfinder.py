import heapq
from utils.position import Position

class Pathfinder:
    def __init__(self, grid):
        self.grid = grid

    def heuristic(self, a: Position, b: Position) -> int:
        # Manhattan distance
        return abs(a.x - b.x) + abs(a.y - b.y)

    def a_star(self, start: Position, goal: Position, body: list[Position]) -> list[Position] | None:
        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}
        occupied = set(body[:-1])  # ignore tail if it will move

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == goal:
                return self._reconstruct_path(came_from, start, goal)

            for next_pos in current.neighbors():
                if not self.grid.is_inside(next_pos):
                    continue
                if next_pos in occupied:
                    continue

                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + self.heuristic(next_pos, goal)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current

        return None  # No path found

    def _reconstruct_path(self, came_from, start, goal) -> list[Position]:
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path
