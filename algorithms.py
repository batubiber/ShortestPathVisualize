import heapq
import numpy as np
from typing import List, Set, Tuple, Optional
from collections import deque

class PathfindingAlgorithm:
    def __init__(self):
        # Separate directions for straight and diagonal movement
        self.straight_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.diagonal_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def is_valid(self, grid: np.ndarray, pos: Tuple[int, int]) -> bool:
        rows, cols = grid.shape
        row, col = pos
        return 0 <= row < rows and 0 <= col < cols and grid[row][col] == 0

    def can_move_diagonally(self, grid: np.ndarray, current: Tuple[int, int], target: Tuple[int, int]) -> bool:
        # Check if both adjacent cells are free for diagonal movement
        dx = target[0] - current[0]
        dy = target[1] - current[1]
        
        # Check the two adjacent cells
        if dx == 1 and dy == 1:  # Moving down-right
            return self.is_valid(grid, (current[0], current[1] + 1)) and self.is_valid(grid, (current[0] + 1, current[1]))
        elif dx == 1 and dy == -1:  # Moving down-left
            return self.is_valid(grid, (current[0], current[1] - 1)) and self.is_valid(grid, (current[0] + 1, current[1]))
        elif dx == -1 and dy == 1:  # Moving up-right
            return self.is_valid(grid, (current[0], current[1] + 1)) and self.is_valid(grid, (current[0] - 1, current[1]))
        elif dx == -1 and dy == -1:  # Moving up-left
            return self.is_valid(grid, (current[0], current[1] - 1)) and self.is_valid(grid, (current[0] - 1, current[1]))
        return True

    def get_neighbors(self, grid: np.ndarray, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        neighbors = []
        
        # Add straight movement neighbors
        for dx, dy in self.straight_directions:
            new_pos = (pos[0] + dx, pos[1] + dy)
            if self.is_valid(grid, new_pos):
                neighbors.append(new_pos)
        
        # Add diagonal movement neighbors if possible
        for dx, dy in self.diagonal_directions:
            new_pos = (pos[0] + dx, pos[1] + dy)
            if self.is_valid(grid, new_pos) and self.can_move_diagonally(grid, pos, new_pos):
                neighbors.append(new_pos)
        
        return neighbors

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

class AStar(PathfindingAlgorithm):
    def find_path(self, grid: np.ndarray, start: Tuple[int, int], 
                 target: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        if not self.is_valid(grid, target):
            return [], []

        open_set = []
        closed_set = set()
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, target)}
        visited = []  # Changed to list to maintain order

        heapq.heappush(open_set, (f_score[start], start))

        while open_set:
            current = heapq.heappop(open_set)[1]
            visited.append(current)  # Add to visited list in order

            if current == target:
                path = self.reconstruct_path(came_from, current)
                return path, visited

            closed_set.add(current)

            for neighbor in self.get_neighbors(grid, current):
                if neighbor in closed_set:
                    continue

                # Calculate distance based on whether it's diagonal or straight movement
                is_diagonal = abs(neighbor[0] - current[0]) == 1 and abs(neighbor[1] - current[1]) == 1
                distance = np.sqrt(2) if is_diagonal else 1
                tentative_g_score = g_score[current] + distance

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, target)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return [], visited

    def reconstruct_path(self, came_from: dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]

class Dijkstra(PathfindingAlgorithm):
    def find_path(self, grid: np.ndarray, start: Tuple[int, int], 
                 target: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        if not self.is_valid(grid, target):
            return [], []

        distances = {start: 0}
        pq = [(0, start)]
        came_from = {}
        visited = []  # Changed to list to maintain order

        while pq:
            current_dist, current = heapq.heappop(pq)
            visited.append(current)  # Add to visited list in order

            if current == target:
                path = self.reconstruct_path(came_from, current)
                return path, visited

            if current_dist > distances[current]:
                continue

            for neighbor in self.get_neighbors(grid, current):
                # Calculate distance based on whether it's diagonal or straight movement
                is_diagonal = abs(neighbor[0] - current[0]) == 1 and abs(neighbor[1] - current[1]) == 1
                distance = np.sqrt(2) if is_diagonal else 1
                new_dist = current_dist + distance

                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    came_from[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))

        return [], visited

    def reconstruct_path(self, came_from: dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]

class GreedyBFS(PathfindingAlgorithm):
    def find_path(self, grid: np.ndarray, start: Tuple[int, int], 
                 target: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        if not self.is_valid(grid, target):
            return [], []

        open_set = [(self.heuristic(start, target), start)]
        came_from = {}
        visited = []  # Changed to list to maintain order
        g_score = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)
            visited.append(current)  # Add to visited list in order

            if current == target:
                path = self.reconstruct_path(came_from, current)
                return path, visited

            for neighbor in self.get_neighbors(grid, current):
                if neighbor not in visited:
                    # Calculate actual distance for better path quality
                    is_diagonal = abs(neighbor[0] - current[0]) == 1 and abs(neighbor[1] - current[1]) == 1
                    distance = np.sqrt(2) if is_diagonal else 1
                    new_g_score = g_score[current] + distance

                    if neighbor not in g_score or new_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = new_g_score
                        # Use a combination of heuristic and actual distance for better path quality
                        f_score = self.heuristic(neighbor, target) + new_g_score
                        heapq.heappush(open_set, (f_score, neighbor))

        return [], visited

    def reconstruct_path(self, came_from: dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1] 