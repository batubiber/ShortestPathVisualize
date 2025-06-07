"""
Pathfinding algorithms implementation module.

This module contains implementations of various pathfinding algorithms:
- A* Algorithm
- Dijkstra's Algorithm
- Greedy Best-First Search
"""

from typing import List, Tuple
import numpy as np

class PathfindingAlgorithm:
    """Base class for pathfinding algorithms."""

    def find_path(self,
                  grid: np.ndarray,
                  start: Tuple[int, int],
                  target: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        """
        Find a path from start to target in the given grid.
        
        Args:
            grid: 2D numpy array representing the grid (0 for empty, 1 for obstacle)
            start: Starting position (row, col)
            target: Target position (row, col)
            
        Returns:
            Tuple containing:
            - List of positions forming the path
            - List of visited positions
        """
        raise NotImplementedError

    def get_neighbors(self, pos: Tuple[int, int], grid: np.ndarray) -> List[Tuple[int, int]]:
        """
        Get valid neighboring positions for a given position.
        
        Args:
            pos: Current position (row, col)
            grid: 2D numpy array representing the grid
            
        Returns:
            List of valid neighboring positions
        """
        row, col = pos
        rows, cols = grid.shape
        neighbors = []
        # Check all 8 directions
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < rows and 0 <= new_col < cols and
                    grid[new_row][new_col] == 0):
                    neighbors.append((new_row, new_col))
        return neighbors

    def heuristic(self, pos: Tuple[int, int], target: Tuple[int, int]) -> float:
        """
        Calculate heuristic value between two positions.
        
        Args:
            pos: Current position (row, col)
            target: Target position (row, col)
            
        Returns:
            Heuristic value (Euclidean distance)
        """
        return ((pos[0] - target[0]) ** 2 + (pos[1] - target[1]) ** 2) ** 0.5

class AStar(PathfindingAlgorithm):
    """A* pathfinding algorithm implementation."""

    def find_path(self,
                  grid: np.ndarray,
                  start: Tuple[int, int],
                  target: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        """
        Find path using A* algorithm.
        
        Args:
            grid: 2D numpy array representing the grid
            start: Starting position (row, col)
            target: Target position (row, col)
            
        Returns:
            Tuple containing:
            - List of positions forming the path
            - List of visited positions
        """
        visited = []
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, target)}
        open_set = {start}

        while open_set:
            current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
            # If the current position is the target, we have found the path
            if current == target:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path, visited

            # Remove the current position from the open set
            open_set.remove(current)
            visited.append(current)

            for neighbor in self.get_neighbors(current, grid):
                tentative_g_score = g_score[current] + self.heuristic(current, neighbor)

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, target)
                    if neighbor not in open_set:
                        open_set.add(neighbor)

        return [], visited

class Dijkstra(PathfindingAlgorithm):
    """Dijkstra's pathfinding algorithm implementation."""

    def find_path(self,
                  grid: np.ndarray,
                  start: Tuple[int, int],
                  target: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        """
        Find path using Dijkstra's algorithm.
        
        Args:
            grid: 2D numpy array representing the grid
            start: Starting position (row, col)
            target: Target position (row, col)
            
        Returns:
            Tuple containing:
            - List of positions forming the path
            - List of visited positions
        """
        visited = []
        distances = {start: 0}
        came_from = {}
        unvisited = {start}

        while unvisited:
            current = min(unvisited, key=lambda x: distances.get(x, float('inf')))

            if current == target:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path, visited

            unvisited.remove(current)
            visited.append(current)

            for neighbor in self.get_neighbors(current, grid):
                distance = distances[current] + self.heuristic(current, neighbor)

                if neighbor not in distances or distance < distances[neighbor]:
                    distances[neighbor] = distance
                    came_from[neighbor] = current
                    unvisited.add(neighbor)

        return [], visited

class GreedyBFS(PathfindingAlgorithm):
    """Greedy Best-First Search algorithm implementation."""

    def find_path(self,
                  grid: np.ndarray,
                  start: Tuple[int, int],
                  target: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        """
        Find path using Greedy Best-First Search algorithm.
        
        Args:
            grid: 2D numpy array representing the grid
            start: Starting position (row, col)
            target: Target position (row, col)
            
        Returns:
            Tuple containing:
            - List of positions forming the path
            - List of visited positions
        """
        visited = []
        came_from = {}
        open_set = {start}

        while open_set:
            current = min(open_set, key=lambda x: self.heuristic(x, target))

            if current == target:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path, visited

            open_set.remove(current)
            visited.append(current)

            for neighbor in self.get_neighbors(current, grid):
                if neighbor not in visited:
                    came_from[neighbor] = current
                    open_set.add(neighbor)

        return [], visited
