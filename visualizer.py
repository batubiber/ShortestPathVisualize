import pygame
import numpy as np
from typing import Dict, List, Optional, Tuple
from algorithms import AStar, Dijkstra, GreedyBFS
from ui_components import Checkbox, TextRenderer, GridRenderer
import time

class PathfindingVisualizer:
    """Main visualization class for pathfinding algorithms."""
    
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Pathfinding Visualizer - All Algorithms")
        
        # Constants
        self.WINDOW_SIZE = 800
        self.GRID_SIZE = 40
        self.COLORS = {
            'WHITE': (255, 255, 255),
            'BLACK': (0, 0, 0),
            'RED': (255, 0, 0),
            'GREEN': (0, 255, 0),
            'BLUE': (0, 0, 255),
            'GRAY': (40, 40, 40),
            'YELLOW': (255, 255, 0),
            'BACKGROUND': (18, 18, 18),
            'TEXT_BG': (0, 0, 0, 200),
            'ASTAR': (255, 165, 0),
            'DIJKSTRA': (0, 255, 255),
            'GREEDY': (255, 192, 203)
        }
        
        # Initialize components
        self.text_renderer = TextRenderer()
        self.grid_renderer = GridRenderer(self.WINDOW_SIZE, self.GRID_SIZE)
        self.initialize_checkboxes()
        
        # Reset state
        self.reset()

    def initialize_checkboxes(self) -> None:
        """Initialize algorithm selection checkboxes."""
        checkbox_x = self.WINDOW_SIZE//2 - 75
        checkbox_y = 400
        self.checkboxes = [
            Checkbox(checkbox_x, checkbox_y, self.COLORS['ASTAR'], "A*"),
            Checkbox(checkbox_x, checkbox_y + 40, self.COLORS['DIJKSTRA'], "Dijkstra"),
            Checkbox(checkbox_x, checkbox_y + 80, self.COLORS['GREEDY'], "Greedy BFS")
        ]

    def reset(self) -> None:
        """Reset the visualization state."""
        self.grid = np.zeros((self.GRID_SIZE, self.GRID_SIZE))
        self.start = None
        self.target = None
        self.setting_start = True
        self.paths = {}
        self.visited = set()
        self.visualizing = False
        self.show_visited = True
        self.drawing = False
        self.max_visited_nodes = 1000
        self.current_algorithm = 0
        self.algorithms = [
            ("A*", AStar()),
            ("Dijkstra", Dijkstra()),
            ("Greedy BFS", GreedyBFS())
        ]
        self.execution_times = {}
        self.algorithm_complete = False
        self.show_start_screen = True
        self.show_warning = False

    def get_selected_algorithms(self) -> List[Tuple[str, object]]:
        """Get list of selected algorithms."""
        return [self.algorithms[i] for i, checkbox in enumerate(self.checkboxes) if checkbox.checked]

    def draw_start_screen(self) -> None:
        """Draw the start screen with instructions."""
        self.screen.fill(self.COLORS['BACKGROUND'])
        
        # Draw title
        title_surface, title_rect = self.text_renderer.render_title("Pathfinding Visualizer", self.COLORS['WHITE'])
        self.screen.blit(title_surface, title_rect)

        # Draw instructions
        instructions = [
            "Instructions:",
            "1. Select at least one algorithm (click checkboxes)",
            "2. Press SPACE to start",
            "3. Right-click to set start point (green)",
            "4. Right-click again to set target point (blue)",
            "5. Left-click to draw/erase obstacles (red)",
            "6. Press SPACE to run selected algorithms",
            "7. Press R to reset",
            "",
            "Algorithm Colors:"
        ]

        y_offset = 100
        for line in instructions:
            text_surface, text_rect = self.text_renderer.render_text(line, self.COLORS['WHITE'], self.WINDOW_SIZE//2, y_offset)
            self.screen.blit(text_surface, text_rect)
            y_offset += 30

        # Draw checkboxes
        for checkbox in self.checkboxes:
            checkbox.draw(self.screen)

        # Draw warning if needed
        if self.show_warning:
            warning_surface, warning_rect = self.text_renderer.render_warning(
                "Please select at least one algorithm!", self.COLORS['RED'])
            self.screen.blit(warning_surface, warning_rect)

        # Draw author name
        author_surface, author_rect = self.text_renderer.render_text(
            "Batuhan Biber", self.COLORS['WHITE'], self.WINDOW_SIZE - 100, self.WINDOW_SIZE - 20)
        self.screen.blit(author_surface, author_rect)

    def draw_grid(self) -> None:
        """Draw the main grid and visualization."""
        self.screen.fill(self.COLORS['BACKGROUND'])
        
        # Draw grid cells
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                if self.grid[i][j] == 1:  # Obstacle
                    self.grid_renderer.draw_cell(self.screen, i, j, self.COLORS['RED'])
                elif self.start and (i, j) == self.start:
                    self.grid_renderer.draw_cell(self.screen, i, j, self.COLORS['GREEN'])
                elif self.target and (i, j) == self.target:
                    self.grid_renderer.draw_cell(self.screen, i, j, self.COLORS['BLUE'])
                elif self.show_visited and (i, j) in self.visited:
                    self.grid_renderer.draw_cell(self.screen, i, j, self.COLORS['YELLOW'])
                else:
                    self.grid_renderer.draw_cell(self.screen, i, j, self.COLORS['BACKGROUND'])

        # Draw complete grid lines
        self.grid_renderer.draw_grid_lines(self.screen)

        # Draw paths if algorithm is complete
        if self.algorithm_complete:
            self.draw_paths()
            self.draw_results_panel()

    def draw_paths(self) -> None:
        """Draw the paths found by each algorithm."""
        for name, _ in self.algorithms:
            if name in self.paths:
                color = (self.COLORS['ASTAR'] if name == "A*" 
                        else self.COLORS['DIJKSTRA'] if name == "Dijkstra" 
                        else self.COLORS['GREEDY'])
                for pos in self.paths[name]:
                    self.grid_renderer.draw_cell(self.screen, pos[0], pos[1], color)

    def draw_results_panel(self) -> None:
        """Draw the results panel showing execution times."""
        panel_surface = pygame.Surface((200, 150), pygame.SRCALPHA)
        panel_surface.fill(self.COLORS['TEXT_BG'])
        self.screen.blit(panel_surface, (self.WINDOW_SIZE - 210, 10))

        y_offset = 20
        for name, _ in self.algorithms:
            if name in self.execution_times:
                color = (self.COLORS['ASTAR'] if name == "A*" 
                        else self.COLORS['DIJKSTRA'] if name == "Dijkstra" 
                        else self.COLORS['GREEDY'])
                text = f"{name}: {self.execution_times[name]:.3f}s"
                text_surface, text_rect = self.text_renderer.render_text(
                    text, color, self.WINDOW_SIZE - 110, y_offset)
                self.screen.blit(text_surface, text_rect)
                y_offset += 30

    def handle_mouse(self, event: pygame.event.Event) -> None:
        """Handle mouse events."""
        if self.show_start_screen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for checkbox in self.checkboxes:
                    checkbox.handle_click(event.pos)
            return

        pos = pygame.mouse.get_pos()
        row, col = self.grid_renderer.get_cell_from_pos(pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if (row, col) != self.start and (row, col) != self.target:
                    self.drawing = True
                    self.grid[row][col] = 1 - self.grid[row][col]
            elif event.button == 3:  # Right click
                if self.grid[row][col] == 0:
                    if self.setting_start:
                        self.start = (row, col)
                        self.setting_start = False
                    else:
                        self.target = (row, col)
                        self.start_visualization()
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.drawing = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.drawing and (row, col) != self.start and (row, col) != self.target:
                self.grid[row][col] = 1

    def start_visualization(self) -> None:
        """Start the pathfinding visualization."""
        self.visualizing = True
        self.paths = {}
        self.visited = set()
        self.show_visited = True
        self.current_algorithm = 0
        self.execution_times = {}
        self.algorithm_complete = False
        self.find_path()

    def find_path(self) -> None:
        """Execute the selected algorithms and visualize their paths."""
        if not (self.start and self.target and not self.algorithm_complete):
            return

        selected_algorithms = self.get_selected_algorithms()
        if not selected_algorithms:
            self.algorithm_complete = True
            self.visualizing = False
            return

        name, algorithm = selected_algorithms[self.current_algorithm]
        
        # Time and execute algorithm
        start_time = time.time()
        path, visited = algorithm.find_path(self.grid, self.start, self.target)
        end_time = time.time()
        
        # Store results
        self.execution_times[name] = end_time - start_time
        self.paths[name] = path
        
        # Animate visited nodes
        self.visited = set()
        for node in visited[:self.max_visited_nodes]:
            self.visited.add(node)
            self.draw_grid()
            pygame.display.flip()
            time.sleep(0.01)
        
        # Move to next algorithm
        self.current_algorithm += 1
        if self.current_algorithm >= len(selected_algorithms):
            self.algorithm_complete = True
            self.visualizing = False
            self.show_visited = False
        else:
            self.visited = set()
            self.show_visited = True
            self.find_path()

    def run(self) -> None:
        """Main application loop."""
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.show_start_screen:
                            if not any(checkbox.checked for checkbox in self.checkboxes):
                                self.show_warning = True
                            else:
                                self.show_warning = False
                                self.show_start_screen = False
                        elif not self.visualizing and self.start and self.target:
                            self.start_visualization()
                    elif event.key == pygame.K_r:
                        self.reset()
                
                if not self.visualizing:
                    self.handle_mouse(event)

            if self.show_start_screen:
                self.draw_start_screen()
            else:
                self.draw_grid()
            pygame.display.flip()

        pygame.quit()