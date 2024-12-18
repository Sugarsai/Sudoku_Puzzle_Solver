import math
import tkinter as tk
from tkinter import messagebox

from solver import solve_sudoku_async  # Assuming this is your original Sudoku solver
from puzzle import generate_random_sudoku, get_hint
from utils import check_location_is_safe
from Generic import genetic_algorithm, fitness, INITIAL_SUDOKU
import puzzle
import utils
import solver
import Generic


def create_board_entries(root, board_size):
    entries = []
    for i in range(board_size):
        row_entries = []
        for j in range(board_size):
            color_index = (i // math.sqrt(board_size) + j // math.sqrt(board_size)) % 2
            entry = tk.Entry(
                root,
                width=5,
                font=("Arial", 18),
                borderwidth=1,
                relief="solid",
                justify="center",
                bg="#FF6347" if color_index == 0 else "#FFD700",
            )
            entry.grid(row=i, column=j, padx=5, pady=5)
            row_entries.append(entry)
        entries.append(row_entries)
    return entries


def show_board_size_selection_window():
    def set_board_size(size):
        global board_size
        board_size = size
        puzzle.board_size = size
        utils.board_size = size
        solver.board_size = size
        Generic.board_size = size
        size_window.destroy()
        create_gui()  # Recreate the GUI with the selected size

    # Create a new window for selecting the board size
    size_window = tk.Tk()
    size_window.title("Select Board Size")

    label = tk.Label(size_window, text="Select Sudoku Board Size", font=("Arial", 14))
    label.pack(pady=10)

    # Buttons for 4x4, 9x9, and 16x16 boards
    button_4x4 = tk.Button(size_window, text="4x4", font=("Arial", 12), command=lambda: set_board_size(4))
    button_4x4.pack(pady=5)

    button_9x9 = tk.Button(size_window, text="9x9", font=("Arial", 12), command=lambda: set_board_size(9))
    button_9x9.pack(pady=5)

    button_16x16 = tk.Button(size_window, text="16x16", font=("Arial", 12), command=lambda: set_board_size(16))
    button_16x16.pack(pady=5)

    size_window.mainloop()


def create_gui():
    def update_gui(arr):
        for i in range(board_size):
            for j in range(board_size):
                entries[i][j].delete(0, tk.END)
                if arr[i][j] != 0:
                    entries[i][j].insert(tk.END, arr[i][j])
        root.update_idletasks()

    def solve_and_display():
        grid = []
        for i in range(board_size):
            row = []
            for j in range(board_size):
                try:
                    value = int(entries[i][j].get())
                    row.append(value if 1 <= value <= board_size else 0)
                except ValueError:
                    row.append(0)
            grid.append(row)

        # Assign grid to INITIAL_SUDOKU for Genetic Solver
        Generic.INITIAL_SUDOKU = [row.copy() for row in grid]

        # Validate initial input
        for i in range(board_size):
            for j in range(board_size):
                if grid[i][j] != 0:
                    num = grid[i][j]
                    grid[i][j] = 0
                    if not check_location_is_safe(grid, i, j, num):
                        messagebox.showerror(
                            "Invalid Input",
                            f"Number {num} at row {i + 1}, column {j + 1} violates Sudoku rules.",
                        )
                        return
                    grid[i][j] = num

        if use_generic_solver.get():
            # Call genetic algorithm with progress_callback
            solution = genetic_algorithm(
                Generic.INITIAL_SUDOKU,
                progress_callback=lambda grid: update_gui(grid)  # GUI update every generation
            )
            if fitness(solution) == 0:
                update_gui(solution)
                messagebox.showinfo("Success", "Sudoku Solved using Genetic Algorithm!")
            else:
                messagebox.showerror("Error", "Failed to solve the Sudoku.")
        else:
            # Original solver logic
            empty_cells = [(row, col) for row in range(board_size) for col in range(board_size) if grid[row][col] == 0]
            SL = []  # Solved cells
            NSL = [(empty_cells[0], 0, [])]  # Next state
            DE = []  # Dead ends
            solve_sudoku_async(grid, empty_cells, SL, NSL, DE, update_gui, root)

    def generate_random_and_display():
        grid = generate_random_sudoku()
        for i in range(board_size):
            for j in range(board_size):
                entries[i][j].delete(0, tk.END)
                if grid[i][j] != 0:
                    entries[i][j].insert(tk.END, grid[i][j])

    def reset_grid():
        for i in range(board_size):
            for j in range(board_size):
                entries[i][j].delete(0, tk.END)

    def hint_and_display():
        grid = []
        for i in range(board_size):
            row = []
            for j in range(board_size):
                try:
                    value = int(entries[i][j].get())
                    row.append(value if 1 <= value <= board_size else 0)
                except ValueError:
                    row.append(0)
            grid.append(row)

        hint = get_hint(grid)
        if hint:
            row, col, num = hint
            messagebox.showinfo("Hint", f"Try placing {num} at row {row + 1}, column {col + 1}.")
        else:
            messagebox.showinfo("Hint", "No empty cells to hint.")

    # Initialize window
    root = tk.Tk()
    root.title("Sudoku Solver")

    entries = create_board_entries(root, board_size)

    # Button frame to structure buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=board_size, column=0, columnspan=board_size, pady=10)

    # Toggle button for selecting the solver
    use_generic_solver = tk.BooleanVar()
    use_generic_solver.set(False)  # Default is to use the original solver

    def toggle_solver():
        use_generic_solver.set(not use_generic_solver.get())
        # Update the button text based on the current state
        if use_generic_solver.get():
            toggle_solver_button.config(text="Switch to Original Solver")
        else:
            toggle_solver_button.config(text="Switch to Genetic Solver")

    toggle_solver_button = tk.Button(
        button_frame,
        text="Switch to Genetic Solver",
        font=("Arial", 14),
        command=toggle_solver,
        bg="lightblue",
        activebackground="blue",
        relief="raised",
        width=22,
    )
    toggle_solver_button.grid(row=0, column=0, padx=5)

    # Solve button
    solve_button = tk.Button(
        button_frame,
        text="Solve",
        font=("Arial", 14),
        command=solve_and_display,
        bg="lightgreen",
        activebackground="green",
        relief="raised",
        width=12,
    )
    solve_button.grid(row=0, column=1, padx=5)

    # Random button
    random_button = tk.Button(
        button_frame,
        text="Random",
        font=("Arial", 14),
        command=generate_random_and_display,
        bg="lightcoral",
        activebackground="red",
        relief="raised",
        width=12,
    )
    random_button.grid(row=0, column=2, padx=5)

    # Reset button
    reset_button = tk.Button(
        button_frame,
        text="Reset",
        font=("Arial", 14),
        command=reset_grid,
        bg="lightblue",
        activebackground="blue",
        relief="raised",
        width=12,
    )
    reset_button.grid(row=1, column=0, columnspan=3, pady=10)

    # Hint button
    hint_button = tk.Button(
        button_frame,
        text="Hint",
        font=("Arial", 14),
        command=hint_and_display,
        bg="lightyellow",
        activebackground="yellow",
        relief="raised",
        width=12,

    )
    hint_button.grid(row=2, column=0, columnspan=3, pady=10)

    root.mainloop()

# Start with the size selection window
show_board_size_selection_window()
