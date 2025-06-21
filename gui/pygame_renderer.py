import pygame
from utils.position import Position

CELL_SIZE = 30
SNAKE_COLOR = (0, 255, 0)
HEAD_COLOR = (0, 200, 0)
APPLE_COLOR = (255, 0, 0)
BG_COLOR = (30, 30, 30)
GRID_COLOR = (50, 50, 50)
BUTTON_COLOR = (70, 70, 200)
TEXT_COLOR = (255, 255, 255)
BUTTON_RADIUS = 12

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

class PygameRenderer:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.simulation_started = False
        self.grid_surface = pygame.Surface((width * CELL_SIZE, height * CELL_SIZE))
        self.window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Smart Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)

        # Centered popup button
        button_width, button_height = 200, 60
        center_x = WINDOW_WIDTH // 2 - button_width // 2
        center_y = WINDOW_HEIGHT // 2 - button_height // 2
        self.button_rect = pygame.Rect(center_x, center_y, button_width, button_height)
        try:
            self.apple_img = pygame.image.load("assets/apple.png").convert_alpha()
            self.apple_img = pygame.transform.scale(self.apple_img, (CELL_SIZE, CELL_SIZE))
        except:
            self.apple_img = None

    def render(self, snake, apple):
        self.window_surface.fill(BG_COLOR)
        self.grid_surface.fill(BG_COLOR)

        # Draw apple
        self._draw_apple(apple.position)

        # Draw snake
        for segment in snake.body[1:]:
            self._draw_cell(segment, SNAKE_COLOR)
        self._draw_cell(snake.head, HEAD_COLOR)

        # Blit grid onto window surface, centered
        grid_rect = self.grid_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.window_surface.blit(self.grid_surface, grid_rect)

        # Draw centered button before simulation starts
        if not self.simulation_started:
            self._draw_popup_button()

        pygame.display.flip()
        self.clock.tick(10)

    def _draw_cell(self, pos: Position, color):
        rect = pygame.Rect(pos.x * CELL_SIZE, pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.grid_surface, color, rect)

    def _draw_apple(self, pos: Position):
        rect = pygame.Rect(pos.x * CELL_SIZE, pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if self.apple_img:
            self.grid_surface.blit(self.apple_img, rect)
        else:
            pygame.draw.rect(self.grid_surface, APPLE_COLOR, rect)

    def _draw_popup_button(self):
        pygame.draw.rect(self.window_surface, BUTTON_COLOR, self.button_rect, border_radius=BUTTON_RADIUS)
        label = self.font.render("Start Simulation", True, TEXT_COLOR)
        label_rect = label.get_rect(center=self.button_rect.center)
        self.window_surface.blit(label, label_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    self.simulation_started = True
        return True
