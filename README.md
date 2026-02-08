# N-Queen Visualizer

A Python Tkinter application that visualizes the N-Queen backtracking algorithm step-by-step.

## Features
- Dynamic **N** input (4 to 10).
- Visual representation of the chessboard and Queens.
- Step-by-step animation of the backtracking algorithm.
- Color-coded states:
    - **Blue**: Placing a Queen.
    - **Green**: Safe position.
    - **Red**: Conflict detected.
    - **Purple**: Backtracking.
- Play/Pause/Step controls and speed adjustment.

## Requirements
- Python 3.x
- Tkinter (usually included with Python)
- Linux (OS Version: linux)

## How to Run

1. Navigate to the project root directory:
   ```bash
   cd ~/n-queen-problem
   ```

2. Run the application as a module:
   ```bash
   python3 -m src.main
   ```

## Controls
- **Start**: Starts the simulation. Uses the locked start column if set.
- **Reset**: Stops and clears the board. Unlocks the start column so you can choose a new one.
- **Pause/Play**: Toggles the automatic animation.
- **Step Forward**: Manually executes the next step (available when paused).
- **Speed Slider**: Adjusts the animation speed (Left = Fast, Right = Slow).
