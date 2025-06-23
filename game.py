import time
from utils.position import Position
from snake import Snake
from apple import Apple
import random
from grid import Grid
from core.snake_planner import SnakePlanner
from gui.pygame_renderer import PygameRenderer

class SnakeGame:
    def __init__(self, grid_width=5, grid_height=5):
        self.grid = Grid(grid_height, grid_width)
        self.snake = Snake(self.grid.center_position())
        self.apples_gained = 0
        self.available_cells = set()
        self.apple = None
        self.planner = SnakePlanner(self.grid)
        self.alive = True
        self.renderer = PygameRenderer(grid_height, grid_width)
        self.current_path = []
        self.visualizing = False
        self.visual_index = 0
        self.waiting_after_eat = False
        self.next_apple_pos = None
        self.status_message = ""
        self.bfs_times = []

    def _random_available_cell(self):
        cells = list(self.available_cells)
        if not cells:
            return None
        return random.choice(cells)

    def plan_path_to_apple(self):
        start_time = time.time()
        path = self.planner.find_safe_path(self.snake, self.apple.position)
        bfs_time = (time.time() - start_time) * 1000
        self.bfs_times.append(bfs_time)
        self.current_path = path if path else []
        self.visualizing = True
        self.visual_index = 0
        self.visual_bfs_order = self.planner.visual_bfs_order.copy()

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
            self.visual_index += 1
            if self.visual_index >= len(self.visual_bfs_order):
                self.visualizing = False
            return
        if self.waiting_after_eat:
            self.available_cells = self._available_cells_after_path(self.current_path)
            self.apple = Apple(self.next_apple_pos)
            if not self.available_cells:
                self.apples_gained += 1
                self.renderer.render(self.snake, self.apple, [], 0, [])
                self.alive = False
                self.status_message = "All cells filled!"
                self.waiting_after_eat = False
                return
            else:
                self.apples_gained += 1
                self.renderer.render(self.snake, self.apple, [], 0, [])
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
                if isinstance(event, tuple) and event[0] == 'start':
                    _, w, h = event
                    self.__init__(w, h)
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
                        self.renderer.render(self.snake, self.apple, self.visual_bfs_order if self.visualizing else [], self.visual_index, self.current_path if not self.visualizing else [])
                    else:
                        self.renderer.render(self.snake, None, [], 0, [])
                    continue
            if self.renderer.simulation_started and self.alive:
                self.step()
            self.renderer.render(self.snake, self.apple, self.visual_bfs_order if self.visualizing else [], self.visual_index, self.current_path if not self.visualizing else [])
            if not self.alive:
                bfs_times = getattr(self, 'bfs_times', [])
                avg_search = sum(bfs_times) / len(bfs_times) if bfs_times else 0
                self.renderer.show_game_over_popup(self.apples_gained, avg_search, getattr(self, 'status_message', None))
                while True:
                    event = self.renderer.handle_events()
                    if event == 'resimulate':
                        self.__init__()
                        first_run = True
                        break
                    if event is False:
                        return