from utils.position import Position

class Pathfinder:
    def __init__(self, grid):
        """Initialize the pathfinder with the given grid."""
        self.grid = grid

    def bnb_path(self, start: Position, goal: Position, body: list[Position]) -> list[Position] | None:
        """Find a path from start to goal using branch-and-bound DFS."""
        occupied = set(body[:-1])  # body excluding tail
        visited = set()
        path = []

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
                    return result  # return first valid safe path found

            return None  # prune path if dead

        return dfs(start, [])
