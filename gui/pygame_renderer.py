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
        """Initialize Pygame renderer and window."""
        pygame.init()
        self.width = width
        self.height = height
        self.simulation_started = False
        self.input_active = False
        self.input_text_w = str(width)
        self.input_text_h = str(height)
        self.input_box_w = pygame.Rect(WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 60, 60, 32)
        self.input_box_h = pygame.Rect(WINDOW_WIDTH // 2 + 20, WINDOW_HEIGHT // 2 - 60, 60, 32)
        self.input_selected = None
        self.cell_size = min(WINDOW_WIDTH // self.width, WINDOW_HEIGHT // self.height)
        self.grid_width = self.width * self.cell_size
        self.grid_height = self.height * self.cell_size
        self.grid_offset_x = (WINDOW_WIDTH - self.grid_width) // 2
        self.grid_offset_y = (WINDOW_HEIGHT - self.grid_height) // 2
        self.window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Smart Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)
        button_width, button_height = 200, 60
        center_x = WINDOW_WIDTH // 2 - button_width // 2
        center_y = WINDOW_HEIGHT // 2 - button_height // 2
        self.button_rect = pygame.Rect(center_x, center_y, button_width, button_height)
        self.algoview_checked = True
        self.algoview_box = pygame.Rect(center_x, center_y - 60, 28, 28)
        try:
            self.apple_img = pygame.image.load("assets/apple.png").convert_alpha()
            self.apple_img = pygame.transform.scale(self.apple_img, (self.cell_size, self.cell_size))

            self.snake_body_img = pygame.image.load("assets/snake_body.png").convert_alpha()
            self.snake_body_img = pygame.transform.scale(self.snake_body_img, (self.cell_size, self.cell_size))

            self.snake_head_img = pygame.image.load("assets/snake_head.png").convert_alpha()
            self.snake_head_img = pygame.transform.scale(self.snake_head_img, (self.cell_size, self.cell_size))
        except:
            self.apple_img = None
            self.snake_body_img = None
            self.snake_head_img = None

    def render(self, snake, apple, visited_cells=None, new_visited=None, final_path=None):
        self.window_surface.fill(BG_COLOR)
        # Draw border
        outer_border = pygame.Rect(
            self.grid_offset_x,
            self.grid_offset_y,
            self.grid_width,
            self.grid_height
        )
        pygame.draw.rect(self.window_surface, (255, 255, 255), outer_border, width=3)
        # Draw all visited cells 
        if visited_cells:
            for pos in visited_cells:
                self._draw_cell(pos, color=(255, 255, 255))
        # Draw final path 
        if final_path:
            for pos in final_path:
                self._draw_cell(pos, color=(255, 255, 0)) 
        # Draw apple
        if apple is not None:
            self._draw_apple(apple.position)
        # Draw snake body
        for segment in snake.body[1:]:
            if self.snake_body_img:
                self._draw_cell(segment, image=self.snake_body_img)
            else:
                self._draw_cell(segment, color=SNAKE_COLOR, outline=True)
        # Draw snake head
        if self.snake_head_img and len(snake.body) > 1:
            dx = snake.head.x - snake.body[1].x
            dy = snake.head.y - snake.body[1].y
            if dx == 1 and dy == 0:
                angle = 270   # Right
            elif dx == -1 and dy == 0:
                angle = 90    # Left
            elif dx == 0 and dy == -1:
                angle = 0     # Up
            elif dx == 0 and dy == 1:
                angle = 180   # Down
            else:
                angle = 0
            rotated_head = pygame.transform.rotate(self.snake_head_img, angle)
            self._draw_cell(snake.head, image=rotated_head)
        else:
            self._draw_cell(snake.head, color=HEAD_COLOR)
        # Button
        if not self.simulation_started:
            self._draw_popup_button()
        pygame.display.flip()
        self.clock.tick(20)

    def _draw_cell(self, pos: Position, color=None, image=None, outline=False):
        rect = pygame.Rect(
            self.grid_offset_x + pos.x * self.cell_size,
            self.grid_offset_y + pos.y * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        if image:
            self.window_surface.blit(image, rect)
        elif color:
            pygame.draw.rect(self.window_surface, color, rect)
            if outline:
                pygame.draw.rect(self.window_surface, (0, 0, 0), rect, width=2)


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
        # Draw input boxes for grid size
        font = self.font
        # Draw container
        container_width, container_height = 260, 120
        container_x = WINDOW_WIDTH // 2 - container_width // 2
        container_y = WINDOW_HEIGHT // 2 - container_height // 2
        container_rect = pygame.Rect(container_x, container_y, container_width, container_height)
        pygame.draw.rect(self.window_surface, (40, 40, 40), container_rect, border_radius=16)
        pygame.draw.rect(self.window_surface, (255,255,255), container_rect, 2, border_radius=16)
        # Draw labels and input boxes
        label_w = font.render("Width:", True, TEXT_COLOR)
        label_h = font.render("Height:", True, TEXT_COLOR)
        self.window_surface.blit(label_w, (container_x + 20, container_y + 20))
        self.window_surface.blit(label_h, (container_x + 20, container_y + 60))
        # Adjust input boxes 
        self.input_box_w.x = container_x + 110
        self.input_box_w.y = container_y + 15
        self.input_box_h.x = container_x + 110
        self.input_box_h.y = container_y + 55
        # Highlight selected input box
        w_color = (0, 255, 255) if self.input_selected == 'w' else (255,255,255)
        h_color = (0, 255, 255) if self.input_selected == 'h' else (255,255,255)
        pygame.draw.rect(self.window_surface, w_color, self.input_box_w, 3)
        pygame.draw.rect(self.window_surface, h_color, self.input_box_h, 3)
        txt_surface_w = font.render(self.input_text_w, True, TEXT_COLOR)
        txt_surface_h = font.render(self.input_text_h, True, TEXT_COLOR)
        self.window_surface.blit(txt_surface_w, (self.input_box_w.x + 5, self.input_box_w.y + 5))
        self.window_surface.blit(txt_surface_h, (self.input_box_h.x + 5, self.input_box_h.y + 5))
        # Draw algorithm view checkbox
        pygame.draw.rect(self.window_surface, (255,255,255), self.algoview_box, 2, border_radius=4)
        if self.algoview_checked:
            pygame.draw.rect(self.window_surface, (255,255,0), self.algoview_box.inflate(-6, -6), border_radius=2)
        algolabel = font.render("Algorithm View", True, TEXT_COLOR)
        self.window_surface.blit(algolabel, (self.algoview_box.right + 10, self.algoview_box.y))
        # Draw simulate button
        mouse_pos = pygame.mouse.get_pos()
        button_color = (100, 100, 255) if self.button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        self.button_rect.x = container_x + 30
        self.button_rect.y = container_y + 90
        pygame.draw.rect(self.window_surface, button_color, self.button_rect, border_radius=BUTTON_RADIUS)
        label = self.font.render("Start Simulation", True, TEXT_COLOR)
        label_rect = label.get_rect(center=self.button_rect.center)
        self.window_surface.blit(label, label_rect)

    def show_game_over_popup(self, apples_gained, avg_search_time, status_message=None):
        """Draw game over popup (stats, status message, resimulate button)"""
        popup_width, popup_height = 300, 140 if status_message else 100
        popup_x = WINDOW_WIDTH // 2 - popup_width // 2
        popup_y = WINDOW_HEIGHT // 2 - popup_height // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(self.window_surface, (40, 40, 40), popup_rect, border_radius=16)
        pygame.draw.rect(self.window_surface, (255, 255, 255), popup_rect, width=2, border_radius=16)
        # Draw stats
        font = pygame.font.SysFont(None, 28)
        label1 = font.render(f"Apples: {apples_gained}", True, (255,255,255))
        label2 = font.render(f"Avg Search: {avg_search_time:.3f} ms", True, (255,255,255))
        self.window_surface.blit(label1, (popup_x + 20, popup_y + 15))
        self.window_surface.blit(label2, (popup_x + 20, popup_y + 45))
        if status_message:
            label3 = font.render(status_message, True, (255,100,100))
            self.window_surface.blit(label3, (popup_x + 20, popup_y + 75))
        # Draw resimulate button 
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(popup_x + 75, popup_y + (popup_height - 34), 150, 24)
        button_color = (100, 100, 255) if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(self.window_surface, button_color, button_rect, border_radius=8)
        button_label = font.render("Re-Simulate", True, TEXT_COLOR)
        button_label_rect = button_label.get_rect(center=button_rect.center)
        self.window_surface.blit(button_label, button_label_rect)
        self.resim_button_rect = button_rect
        pygame.display.flip()

    def show_invalid_popup(self, message="Invalid grid size!"):
        popup_width, popup_height = 260, 80
        popup_x = WINDOW_WIDTH // 2 - popup_width // 2
        popup_y = WINDOW_HEIGHT // 2 - popup_height // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(self.window_surface, (40, 40, 40), popup_rect, border_radius=16)
        pygame.draw.rect(self.window_surface, (255, 100, 100), popup_rect, width=2, border_radius=16)
        font = pygame.font.SysFont(None, 28)
        label = font.render(message, True, (255, 100, 100))
        self.window_surface.blit(label, (popup_x + 20, popup_y + 25))
        pygame.display.flip()
        pygame.time.wait(1200)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if not self.simulation_started:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box_w.collidepoint(event.pos):
                        self.input_selected = 'w'
                    elif self.input_box_h.collidepoint(event.pos):
                        self.input_selected = 'h'
                    elif self.algoview_box.collidepoint(event.pos):
                        self.algoview_checked = not self.algoview_checked
                    else:
                        self.input_selected = None
                    if self.button_rect.collidepoint(event.pos):
                        w = int(self.input_text_w)
                        h = int(self.input_text_h)
                        if (w, h) in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                            self.show_invalid_popup()
                            return True
                        self.simulation_started = True
                        return ('start', w, h, self.algoview_checked)
                if event.type == pygame.KEYDOWN and self.input_selected:
                    if event.key == pygame.K_BACKSPACE:
                        if self.input_selected == 'w':
                            self.input_text_w = self.input_text_w[:-1]
                        elif self.input_selected == 'h':
                            self.input_text_h = self.input_text_h[:-1]
                    elif event.unicode.isdigit():
                        if self.input_selected == 'w' and len(self.input_text_w) < 3:
                            if self.input_text_w == '0':
                                self.input_text_w = event.unicode
                            else:
                                self.input_text_w += event.unicode
                        elif self.input_selected == 'h' and len(self.input_text_h) < 3:
                            if self.input_text_h == '0':
                                self.input_text_h = event.unicode
                            else:
                                self.input_text_h += event.unicode
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hasattr(self, 'resim_button_rect') and self.resim_button_rect.collidepoint(event.pos):
                        return 'resimulate'
        return True
