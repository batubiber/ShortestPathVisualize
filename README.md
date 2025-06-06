# Pathfinding Visualizer

A Python-based visualization tool that demonstrates and compares different pathfinding algorithms in action. The application provides an interactive grid where users can set start and target points, create obstacles, and observe how different algorithms find the optimal path.

## Features

- Interactive grid-based visualization
- Multiple pathfinding algorithms:
  - A* Algorithm
  - Dijkstra's Algorithm
  - Greedy Best-First Search
- Real-time algorithm execution time comparison
- Customizable algorithm selection
- Visual representation of:
  - Start point (green)
  - Target point (blue)
  - Obstacles (red)
  - Visited nodes (yellow)
  - Algorithm paths (unique colors for each algorithm)

## Requirements

- Python 3.8+
- Pygame
- NumPy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pathfinding-visualizer.git
cd pathfinding-visualizer
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. On the start screen:
   - Select one or more algorithms using the checkboxes
   - Press SPACE to begin

3. In the visualization:
   - Right-click to set the start point (green)
   - Right-click again to set the target point (blue)
   - Left-click to draw/erase obstacles (red)
   - Press SPACE to run the selected algorithms
   - Press R to reset the grid

## Project Structure

```
pathfinding-visualizer/
├── main.py              # Main application and visualization logic
├── algorithms.py        # Pathfinding algorithm implementations
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## Implementation Details

The project follows SOLID principles:

- **Single Responsibility Principle**: Each class has a single responsibility
  - `PathfindingVisualizer`: Handles visualization and user interaction
  - `Checkbox`: Manages checkbox UI elements
  - Algorithm classes: Implement specific pathfinding logic

- **Open/Closed Principle**: The code is open for extension but closed for modification
  - New algorithms can be added by extending the base `PathfindingAlgorithm` class
  - UI elements can be extended without modifying existing code

- **Liskov Substitution Principle**: Algorithm implementations are interchangeable
  - All algorithms inherit from `PathfindingAlgorithm`
  - They can be used interchangeably in the visualization

- **Interface Segregation Principle**: Classes have specific interfaces
  - UI elements have focused interfaces
  - Algorithm classes expose only necessary methods

- **Dependency Inversion Principle**: High-level modules don't depend on low-level modules
  - Visualization depends on algorithm abstractions
  - UI components are loosely coupled

## Author

Batuhan Biber

## License

This project is licensed under the MIT License - see the LICENSE file for details.