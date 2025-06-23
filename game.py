import time
from utils.position import Position
from snake import Snake
from apple import Apple
import random
from grid import Grid
from core.snake_planner import SnakePlanner
from gui.pygame_renderer import PygameRenderer

GRID_HEIGHT = 7
GRID_WIDTH = 5

class SnakeGame:
    def __init__(self):
        """Initialize the main game state and components."""
        self.grid = Grid(GRID_HEIGHT, GRID_WIDTH)
        self.snake = Snake(self.grid.center_position())
        self.apple = Apple(self.grid.random_empty_position(self.snake))
        self.planner = SnakePlanner(self.grid)
        self.alive = True
        self.renderer = PygameRenderer(GRID_HEIGHT, GRID_WIDTH)
        self.current_path = []
        self.visualizing = False
        self.visual_index = 0
        self.waiting_after_eat = False  
        self.next_apple_pos = None
        self.plan_path_to_apple()

    def plan_path_to_apple(self):
        """Plan a path from the snake to the apple using the planner."""
        path = self.planner.find_safe_path(self.snake, self.apple.position)
        self.current_path = path if path else []
        self.visualizing = True
        self.visual_index = 0
        self.visual_bfs_order = self.planner.visual_bfs_order.copy()
        if not self.current_path:
            self.alive = False

    def step(self):
        """Advance the game by one step, handling movement and visualization."""
        if self.visualizing:
            self.visual_index += 1
            if self.visual_index >= len(self.visual_bfs_order):
                self.visualizing = False
            return
        if self.waiting_after_eat:
            self.apple = Apple(self.next_apple_pos)
            self.plan_path_to_apple()
            self.waiting_after_eat = False
            return
        if not self.current_path:
            self.alive = False
            return
        next_move = self.current_path.pop(0)
        self.snake.move_towards(next_move)
        if self.snake.head == self.apple.position:
            # If this is the first apple eaten (snake length 1), set direction to the last move just made
            if len(self.snake.body) == 1:
                self.snake.grow(direction=self.snake.last_direction)
            else:
                self.snake.grow()
            pos = self.find_reachable_apple_position()
            if pos:
                self.next_apple_pos = pos
                self.waiting_after_eat = True
            else:
                self.alive = False

    def find_reachable_apple_position(self):
        """Find a reachable position for the apple that is not occupied by the snake."""
        candidates = [
            Position(x, y)
            for x in range(self.grid.width)
            for y in range(self.grid.height)
            if Position(x, y) not in self.snake.body
        ]
        random.shuffle(candidates)
        for pos in candidates:
            test_path = self.planner.find_safe_path(self.snake, pos)
            if test_path:
                return pos
        return None

    def run(self):
        """Run the main game loop until the game is over or exited."""
        while True:
            if not self.renderer.handle_events():
                break
            if self.renderer.simulation_started and self.alive:
                self.step()
            self.renderer.render(self.snake, self.apple, self.visual_bfs_order if self.visualizing else [], self.visual_index, self.current_path if not self.visualizing else [])