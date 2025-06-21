import time
from utils.position import Position
from snake import Snake
from apple import Apple
from grid import Grid
from core.snake_planner import SnakePlanner
from gui.pygame_renderer import PygameRenderer

GRID_HEIGHT = 25
GRID_WIDTH = 30

class SnakeGame:
    def __init__(self):
        self.grid = Grid(GRID_HEIGHT, GRID_WIDTH)
        self.snake = Snake(self.grid.center_position())
        self.apple = Apple(self.grid.random_empty_position(self.snake))
        self.planner = SnakePlanner(self.grid)
        self.alive = True
        self.renderer = PygameRenderer(GRID_WIDTH, GRID_HEIGHT)

    def step(self):
        path = self.planner.find_safe_path(self.snake, self.apple.position)
        if not path:
            print("⚠ No path found, game over")
            self.alive = False
            return

        next_move = path[0]        
        self.snake.move_towards(next_move)

        if self.snake.head == self.apple.position:
            self.snake.grow()
            self.apple = Apple(self.grid.random_empty_position(self.snake))

    def run(self):
        while True:
            if not self.renderer.handle_events():
                break

            if self.renderer.simulation_started and self.alive:
                self.step()

            self.renderer.render(self.snake, self.apple)
            time.sleep(0.05)