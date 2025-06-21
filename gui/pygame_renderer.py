# gui/pygame_renderer.py
import pygame
from utils.position import Position

SNAKE_COLOR = (0, 255, 0)
HEAD_COLOR = (0, 200, 0)
APPLE_COLOR = (255, 0, 0)
BG_COLOR = (30, 30, 30)
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

        # Adjust cell size to fully fit grid in window
        self.cell_size = min(
            WINDOW_WIDTH // self.width,
            WINDOW_HEIGHT // self.height
        )
        self.grid_width = self.width * self.cell_size
        self.grid_height = self.height * self.cell_size

        # Offset to center the grid
        self.grid_offset_x = (WINDOW_WIDTH - self.grid_width) // 2
        self.grid_offset_y = (WINDOW_HEIGHT - self.grid_height) // 2

        self.window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Smart Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)

        # Button rect (centered popup)
        button_width, button_height = 200, 60
        center_x = WINDOW_WIDTH // 2 - button_width // 2
        center_y = WINDOW_HEIGHT // 2 - button_height // 2
        self.button_rect = pygame.Rect(center_x, center_y, button_width, button_height)

        try:
            self.apple_img = pygame.image.load("assets/apple.png").convert_alpha()
            self.apple_img = pygame.transform.scale(self.apple_img, (self.cell_size, self.cell_size))
        except:
            self.apple_img = None

    def render(self, snake, apple):
        self.window_surface.fill(BG_COLOR)

        # Draw apple
        self._draw_apple(apple.position)

        # Draw snake
        for segment in snake.body[1:]:
            self._draw_cell(segment, SNAKE_COLOR)
        self._draw_cell(snake.head, HEAD_COLOR)

        # Button (only before start)
        if not self.simulation_started:
            self._draw_popup_button()

        pygame.display.flip()
        self.clock.tick(10)

    def _draw_cell(self, pos: Position, color):
        rect = pygame.Rect(
            self.grid_offset_x + pos.x * self.cell_size,
            self.grid_offset_y + pos.y * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        pygame.draw.rect(self.window_surface, color, rect)

    def _draw_apple(self, pos: Position):
        rect = pygame.Rect(
            self.grid_offset_x + pos.x * self.cell_size,
            self.grid_offset_y + pos.y * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        if self.apple_img:
            self.window_surface.blit(self.apple_img, rect)
        else:
            pygame.draw.rect(self.window_surface, APPLE_COLOR, rect)

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
