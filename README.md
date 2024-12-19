# Sudoku Puzzle Solver

Welcome to the **Sudoku Puzzle Solver** repository! This repository contains implementations of algorithms to solve Sudoku puzzles using **Backtracking** and **Genetic Algorithms**. The focus is on clarity, efficiency, and adaptability for different Sudoku variations.

## Project Introduction

This project implements a Sudoku Puzzle Solver utilizing two distinct approaches:

- **Backtracking Algorithm**: A systematic and recursive method to explore all possible puzzle configurations.
- **Genetic Algorithm**: An evolutionary approach inspired by natural selection to find optimized solutions.

### What is Sudoku?

Sudoku is a well-known number-placement puzzle where a grid (commonly 9x9, but variations like 4x4 and 16x16 are also supported) must be filled with digits such that:

1. Each row contains all digits without repetition.
2. Each column contains all digits without repetition.
3. Each subgrid (e.g., 3x3 for 9x9 puzzles) contains all digits without repetition.

The solver efficiently tackles Sudoku puzzles by exploring possible configurations and finding the correct combination that satisfies all constraints.

---

## Development Platform

- **Python**: Version 3.12.6
- **Tkinter**: For GUI
- **Matplotlib.pyplot**: For visualization

---

## Project Overview

The project is organized into multiple Python modules for modularity and clarity:

### backtracking.py
- Implements the Backtracking algorithm for Sudoku solving.
- Recursively fills the grid, backtracks on incorrect placements, and continues until a valid solution is found.

### generic.py
- Implements Genetic Algorithms to iteratively improve solutions by simulating natural selection.
- Favors fit individuals and introduces genetic variation through crossover and mutation.

### gui.py
- Provides a graphical user interface for the Sudoku Solver.
- Allows users to input puzzles, visualize solutions, and interact with the solver.

### main.py
- Serves as the entry point of the project.

### puzzle.py
- Contains functions to generate Sudoku puzzles and provide hints.

### utils.py
- Contains helper functions for Sudoku operations.
- Includes functionality to check if a given number can be placed at a specific location by verifying that it doesn't conflict with existing numbers in the same row, column, or subgrid.
- Supports grids of varying sizes (e.g., 4x4, 9x9, 16x16).

---

## Features

- **Solves standard and custom Sudoku grids** (e.g., 4x4, 9x9, 16x16).
- **Interactive GUI** for puzzle input and visualization.
- Includes both **Backtracking** and **Genetic Algorithm** approaches.
- Generates puzzles and provides hints for unsolved grids.

---

## Usage

To run the project:
```bash
python main.py
```

### Input
- GUI Provide random Sudoku grid.

### Output
- A completed Sudoku grid displayed in the GUI.

---

## License

This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Team Members:
- Sara Ashraf
- Omar Ahmed
- Refaat Ismail
- Sara Ahmed 
- Ali Gomaa
- Ahmed Maghawry
