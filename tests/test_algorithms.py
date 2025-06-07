import pytest
import numpy as np
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms import AStar, Dijkstra, GreedyBFS

def create_test_grid():
    """Create a 5x5 grid with no obstacles."""
    return np.zeros((5, 5))

def create_grid_with_obstacles():
    """Create a 5x5 grid with obstacles blocking the diagonal path."""
    grid = np.zeros((5, 5))
    # Add obstacles in the middle
    grid[1:4, 1:4] = 1
    # Leave a path around the obstacles
    grid[0, :] = 0
    grid[4, :] = 0
    grid[:, 0] = 0
    grid[:, 4] = 0
    return grid

def create_no_path_grid():
    """Create a 5x5 grid with no valid path from start to target."""
    grid = np.zeros((5, 5))
    # Create a wall between start and target
    grid[2, :] = 1
    return grid

@pytest.fixture
def grid():
    return create_test_grid()

@pytest.fixture
def grid_with_obstacles():
    return create_grid_with_obstacles()

@pytest.fixture
def no_path_grid():
    return create_no_path_grid()

@pytest.fixture
def start():
    return (0, 0)

@pytest.fixture
def target():
    return (4, 4)

@pytest.fixture
def alternate_start():
    return (0, 4)

@pytest.fixture
def alternate_target():
    return (4, 0)

def test_astar_path(grid, start, target):
    """Test A* algorithm finds a valid path in empty grid."""
    astar = AStar()
    path, _ = astar.find_path(grid, start, target)
    
    # Check path exists
    assert path is not None
    # Check path starts and ends correctly
    assert path[0] == start
    assert path[-1] == target
    # Check path length (should be 5 for diagonal path in 5x5 grid)
    assert len(path) == 5
    # Check path is continuous
    for i in range(len(path) - 1):
        current = path[i]
        next_pos = path[i + 1]
        # Check if adjacent (including diagonals)
        assert abs(current[0] - next_pos[0]) <= 1
        assert abs(current[1] - next_pos[1]) <= 1

def test_astar_with_obstacles(grid_with_obstacles, start, target):
    """Test A* algorithm finds a valid path around obstacles."""
    astar = AStar()
    path, _ = astar.find_path(grid_with_obstacles, start, target)
    
    assert path is not None
    assert path[0] == start
    assert path[-1] == target
    
    # Check path doesn't go through obstacles
    for pos in path:
        assert grid_with_obstacles[pos] == 0

def test_astar_no_path(no_path_grid, start, target):
    """Test A* algorithm handles no valid path case."""
    astar = AStar()
    path, _ = astar.find_path(no_path_grid, start, target)
    assert path == []  # Empty list indicates no path found

def test_astar_alternate_path(grid, alternate_start, alternate_target):
    """Test A* algorithm with different start/end positions."""
    astar = AStar()
    path, _ = astar.find_path(grid, alternate_start, alternate_target)
    
    assert path is not None
    assert path[0] == alternate_start
    assert path[-1] == alternate_target
    assert len(path) == 5

def test_dijkstra_path(grid, start, target):
    """Test Dijkstra's algorithm finds a valid path in empty grid."""
    dijkstra = Dijkstra()
    path, _ = dijkstra.find_path(grid, start, target)
    
    assert path is not None
    assert path[0] == start
    assert path[-1] == target
    assert len(path) == 5
    
    for i in range(len(path) - 1):
        current = path[i]
        next_pos = path[i + 1]
        assert abs(current[0] - next_pos[0]) <= 1
        assert abs(current[1] - next_pos[1]) <= 1

def test_dijkstra_with_obstacles(grid_with_obstacles, start, target):
    """Test Dijkstra's algorithm finds a valid path around obstacles."""
    dijkstra = Dijkstra()
    path, _ = dijkstra.find_path(grid_with_obstacles, start, target)
    
    assert path is not None
    assert path[0] == start
    assert path[-1] == target
    
    for pos in path:
        assert grid_with_obstacles[pos] == 0

def test_dijkstra_no_path(no_path_grid, start, target):
    """Test Dijkstra's algorithm handles no valid path case."""
    dijkstra = Dijkstra()
    path, _ = dijkstra.find_path(no_path_grid, start, target)
    assert path == []  # Empty list indicates no path found

def test_greedy_bfs_path(grid, start, target):
    """Test Greedy BFS algorithm finds a valid path in empty grid."""
    greedy = GreedyBFS()
    path, _ = greedy.find_path(grid, start, target)
    
    assert path is not None
    assert path[0] == start
    assert path[-1] == target
    assert len(path) == 5
    
    for i in range(len(path) - 1):
        current = path[i]
        next_pos = path[i + 1]
        assert abs(current[0] - next_pos[0]) <= 1
        assert abs(current[1] - next_pos[1]) <= 1

def test_greedy_bfs_with_obstacles(grid_with_obstacles, start, target):
    """Test Greedy BFS algorithm finds a valid path around obstacles."""
    greedy = GreedyBFS()
    path, _ = greedy.find_path(grid_with_obstacles, start, target)
    
    assert path is not None
    assert path[0] == start
    assert path[-1] == target
    
    for pos in path:
        assert grid_with_obstacles[pos] == 0

def test_greedy_bfs_no_path(no_path_grid, start, target):
    """Test Greedy BFS algorithm handles no valid path case."""
    greedy = GreedyBFS()
    path, _ = greedy.find_path(no_path_grid, start, target)
    assert path == []  # Empty list indicates no path found 
