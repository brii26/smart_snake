import pygame
from utils.position import Position

CELL_SIZE = 30
SNAKE_COLOR = (0, 255, 0)
HEAD_COLOR = (0, 200, 0)
APPLE_COLOR = (255, 0, 0)
BG_COLOR = (30, 30, 30)
GRID_COLOR = (50, 50, 50)

class PygameRenderer:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width * CELL_SIZE, height * CELL_SIZE))
        pygame.display.set_caption("Smart Snake")
        self.clock = pygame.time.Clock()

    def render(self, snake, apple):
        self.screen.fill(BG_COLOR)

        # Draw grid
        for x in range(self.width):
            for y in range(self.height):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

        # Draw apple
        self._draw_cell(apple.position, APPLE_COLOR)

        # Draw snake
        for segment in snake.body[1:]:
            self._draw_cell(segment, SNAKE_COLOR)
        self._draw_cell(snake.head, HEAD_COLOR)

        pygame.display.flip()
        self.clock.tick(10)  # Limit to 10 FPS

    def _draw_cell(self, pos: Position, color):
        rect = pygame.Rect(pos.x * CELL_SIZE, pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
