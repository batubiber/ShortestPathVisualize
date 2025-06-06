import pygame
from typing import Tuple, List, Optional

class Checkbox:
    """A UI component for selecting algorithms."""
    def __init__(self, x: int, y: int, color: Tuple[int, int, int], name: str):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = color
        self.name = name
        self.checked = False

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the checkbox and its label."""
        pygame.draw.rect(screen, self.color, self.rect, 2)
        if self.checked:
            pygame.draw.rect(screen, self.color, self.rect.inflate(-4, -4))
        
        text = pygame.font.SysFont('Arial', 20).render(self.name, True, self.color)
        screen.blit(text, (self.rect.right + 5, self.rect.y))

    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """Handle click events on the checkbox."""
        if self.rect.collidepoint(pos):
            self.checked = not self.checked
            return True
        return False

class TextRenderer:
    """Handles text rendering for the application."""
    def __init__(self):
        self.title_font = pygame.font.SysFont('Arial', 30, bold=True)
        self.normal_font = pygame.font.SysFont('Arial', 20)
        self.warning_font = pygame.font.SysFont('Arial', 24, bold=True)

    def render_title(self, text: str, color: Tuple[int, int, int]) -> Tuple[pygame.Surface, pygame.Rect]:
        """Render a title text."""
        surface = self.title_font.render(text, True, color)
        rect = surface.get_rect(center=(800//2, 50))
        return surface, rect

    def render_text(self, text: str, color: Tuple[int, int, int], center_x: int, y: int) -> Tuple[pygame.Surface, pygame.Rect]:
        """Render normal text."""
        surface = self.normal_font.render(text, True, color)
        rect = surface.get_rect(center=(center_x, y))
        return surface, rect

    def render_warning(self, text: str, color: Tuple[int, int, int]) -> Tuple[pygame.Surface, pygame.Rect]:
        """Render warning text."""
        surface = self.warning_font.render(text, True, color)
        rect = surface.get_rect(center=(800//2, 700))
        return surface, rect

class GridRenderer:
    """Handles grid rendering and cell operations."""
    def __init__(self, window_size: int, grid_size: int):
        self.window_size = window_size
        self.grid_size = grid_size
        self.cell_size = window_size // grid_size
        self.grid_color = (40, 40, 40)  # Dark gray for grid lines

    def get_cell_from_pos(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Convert screen position to grid coordinates."""
        x, y = pos
        row = min(max(y // self.cell_size, 0), self.grid_size - 1)
        col = min(max(x // self.cell_size, 0), self.grid_size - 1)
        return row, col

    def draw_cell(self, screen: pygame.Surface, row: int, col: int, color: Tuple[int, int, int]) -> None:
        """Draw a single cell in the grid."""
        rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
        # Draw cell background
        pygame.draw.rect(screen, color, rect)
        # Draw grid lines on top
        pygame.draw.rect(screen, self.grid_color, rect, 1)

    def draw_grid_lines(self, screen: pygame.Surface) -> None:
        """Draw the complete grid lines."""
        # Draw vertical lines
        for x in range(0, self.window_size + 1, self.cell_size):
            pygame.draw.line(screen, self.grid_color, (x, 0), (x, self.window_size))
        # Draw horizontal lines
        for y in range(0, self.window_size + 1, self.cell_size):
            pygame.draw.line(screen, self.grid_color, (0, y), (self.window_size, y))