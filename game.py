import time
from utils.position import Position
from snake import Snake
from apple import Apple
from grid import Grid
from core.snake_planner import SnakePlanner
from gui.pygame_renderer import PygameRenderer

GRID_SIZE = 15

class SnakeGame:
    def __init__(self):
        self.grid = Grid(GRID_SIZE, GRID_SIZE)
        self.snake = Snake(self.grid.center_position())
        self.apple = Apple(self.grid.random_empty_position(self.snake))
        self.planner = SnakePlanner(self.grid)
        self.alive = True
        self.renderer = PygameRenderer(self.grid.width, self.grid.height)

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
        while self.alive:
            if not self.renderer.handle_events():
                break
            self.step()
            self.renderer.render(self.snake, self.apple)
            time.sleep(0.1)

    def print_state(self):
        print("\033[H\033[J", end="")  # clear terminal
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                pos = Position(x, y)
                if pos == self.snake.head:
                    print("H", end=" ")
                elif pos in self.snake.body:
                    print("o", end=" ")
                elif pos == self.apple.position:
                    print("A", end=" ")
                else:
                    print(".", end=" ")
            print()