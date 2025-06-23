import time
from utils.position import Position
from snake import Snake
from apple import Apple
import random
from grid import Grid
from core.pathfinder import Pathfinder
from core.pathfinding_utils import PathfindingUtils
from gui.pygame_renderer import PygameRenderer


class SnakeGame:
    def __init__(self, grid_width=7, grid_height=7, visualize=True):
        self.grid = Grid(grid_height, grid_width)
        self.snake = Snake(self.grid.center_position())
        self.apples_gained = 0
        self.available_cells = set()
        self.apple = None
        self.pathfinder = Pathfinder(self.grid)
        self.utils = PathfindingUtils(self.grid)
        self.alive = True
        self.renderer = PygameRenderer(grid_height, grid_width)
        self.current_path = []
        self.visualizing = False
        self.visual_index = 0
        self.waiting_after_eat = False
        self.next_apple_pos = None
        self.status_message = ""
        self.bfs_times = []
        self.show_final_path = False
        self.final_path_to_show = []
        self.visualize = visualize

    def _random_available_cell(self):
        cells = list(self.available_cells)
        if not cells:
            return None
        return random.choice(cells)

    def plan_path_to_apple(self):
        if self.visualize:
            self.astar_gen = self.utils.astar_generator(
                self.snake, self.apple.position, batch_size=1
            )
            self.bfs_visited = set()
            self.bfs_found_path = None
            self.visualizing = True
            self.visual_bfs_order = []
            self.bfs_new_cells = []
            self.current_path = []
        else:
            start = time.perf_counter()
            path, _ = self.pathfinder.astar_path(self.snake, self.apple.position)
            elapsed = (time.perf_counter() - start) * 1000
            self.bfs_times.append(elapsed)
            self.current_path = path if path else []
            self.visualizing = False
            self.bfs_visited = set()
            self.bfs_found_path = None
            self.visual_bfs_order = []
            self.bfs_new_cells = []

    def _available_cells_after_path(self, path):
        sim_snake = self.snake.copy()
        for move in path:
            sim_snake.move_towards(move)
        if path and sim_snake.head == self.apple.position:
            if len(sim_snake.body) == 1:
                sim_snake.grow(direction=sim_snake.last_direction)
            else:
                sim_snake.grow()
        return set(
            Position(x, y)
            for x in range(self.grid.width)
            for y in range(self.grid.height)
            if Position(x, y) not in sim_snake.body
        )

    def _recompute_available_cells(self):
        self.available_cells = set(
            Position(x, y)
            for x in range(self.grid.width)
            for y in range(self.grid.height)
            if Position(x, y) not in self.snake.body
        )

    def step(self):
        if self.visualizing:
            try:
                visited, current_path, found_path = next(self.astar_gen)
                new_cells = set(visited) - self.bfs_visited
                self.bfs_visited |= new_cells
                self.visual_bfs_order = list(self.bfs_visited)
                self.bfs_new_cells = list(new_cells)
                if found_path is not None:
                    self.current_path = found_path
                    self.visualizing = False
                    self.show_final_path = True
                    self.final_path_to_show = list(found_path)
            except StopIteration:
                self.visualizing = False
                self.bfs_new_cells = []
            return
        if self.show_final_path:
            self.bfs_visited = set()
            self.show_final_path = False
            return
        if self.waiting_after_eat:
            self.available_cells = self._available_cells_after_path(self.current_path)
            self.apple = Apple(self.next_apple_pos)
            if not self.available_cells:
                self.apples_gained += 1
                self.renderer.render(self.snake, self.apple, [], [])
                self.alive = False
                self.status_message = "All cells filled!"
                self.waiting_after_eat = False
                return
            else:
                self.apples_gained += 1
                self.renderer.render(self.snake, self.apple, [], [])
                self.plan_path_to_apple()
                self.waiting_after_eat = False
                return
        if not self.current_path:
            if self.snake.head == self.apple.position:
                if len(self.snake.body) == 1:
                    self.snake.grow(direction=self.snake.last_direction)
                else:
                    self.snake.grow()
                self._recompute_available_cells()
                if self.available_cells:
                    self.next_apple_pos = self._random_available_cell()
                    self.waiting_after_eat = True
                    return
                else:
                    self.next_apple_pos = self.snake.head
                    self.waiting_after_eat = True
                    return
            if not self.available_cells:
                self.alive = False
                self.status_message = "No cells available for apple."
            else:
                self.alive = False
                self.status_message = "Apple unreachable."
            return
        next_move = self.current_path.pop(0)
        growing = (self.snake.head == self.apple.position)
        self.snake.move_towards(next_move)
        if growing:
            if len(self.snake.body) == 1:
                self.snake.grow(direction=self.snake.last_direction)
            else:
                self.snake.grow()
            self._recompute_available_cells()
            if self.available_cells:
                self.next_apple_pos = self._random_available_cell()
                self.waiting_after_eat = True
                return
            else:
                self.next_apple_pos = self.snake.head
                self.waiting_after_eat = True
                return
        else:
            self._recompute_available_cells()
            self.status_message = ""

    def run(self):
        first_run = True
        self.status_message = ""
        while True:
            event = self.renderer.handle_events()
            if event is False:
                break
            if first_run:
                if isinstance(event, tuple) and event[0] == "start":
                    _, w, h, algoview = event if len(event) == 4 else (*event, True)
                    self.__init__(w, h, visualize=algoview)
                    self.available_cells = set(
                        Position(x, y)
                        for x in range(self.grid.width)
                        for y in range(self.grid.height)
                        if Position(x, y) != self.snake.head
                    )
                    self.apple = Apple(self._random_available_cell())
                    self.plan_path_to_apple()
                    first_run = False
                    self.renderer.simulation_started = True
                else:
                    if self.apple is not None:
                        self.renderer.render(
                            self.snake,
                            self.apple,
                            visited_cells=getattr(self, "bfs_visited", set()),
                            final_path=self.current_path if not self.visualizing else [],
                        )
                    else:
                        self.renderer.render(self.snake, None, visited_cells=set(), final_path=[])
                    continue
            if self.renderer.simulation_started and self.alive:
                self.step()
            if self.visualize and self.show_final_path:
                self.renderer.render(
                    self.snake,
                    self.apple,
                    visited_cells=set(),
                    final_path=self.final_path_to_show,
                )
            elif self.visualize:
                self.renderer.render(
                    self.snake,
                    self.apple,
                    visited_cells=getattr(self, "bfs_visited", set()),
                    final_path=self.current_path if not self.visualizing else [],
                )
            else:
                self.renderer.render(
                    self.snake,
                    self.apple,
                    visited_cells=set(),
                    final_path=[],
                )
            self.bfs_new_cells = []
            if not self.alive:
                bfs_times = getattr(self, "bfs_times", [])
                avg_search = sum(bfs_times) / len(bfs_times) if bfs_times else 0
                self.renderer.show_game_over_popup(
                    self.apples_gained, avg_search, getattr(self, "status_message", None)
                )
                while True:
                    event = self.renderer.handle_events()
                    if event == "resimulate":
                        self.__init__()
                        first_run = True
                        break
                    if event is False:
                        return