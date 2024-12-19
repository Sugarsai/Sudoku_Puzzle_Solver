import math
import threading
import tkinter as tk
from tkinter import messagebox

from puzzle import generate_random_sudoku, get_hint
from utils import check_location_is_safe
from Generic import genetic_algorithm, fitness
import puzzle
import utils
import backtracking
import Generic

def create_board_entries(frame, board_size):
    """Create a grid of Tkinter entries for Sudoku."""
    entries = []
    for i in range(board_size):
        row_entries = []
        for j in range(board_size):
            color_index = (i // math.sqrt(board_size) + j // math.sqrt(board_size)) % 2
            entry = tk.Entry(
                frame,
                width=3,
                font=("Arial", 10),
                borderwidth=1,
                relief="solid",
                justify="center",
                bg="#FF6347" if color_index == 0 else "#FFD700",
            )
            entry.grid(row=i, column=j, padx=5, pady=5)
            row_entries.append(entry)
        entries.append(row_entries)
    return entries

def show_board_size_selection_window(root, frame):
    """Display the board size selection interface."""
    for widget in frame.winfo_children():
        widget.destroy()

    def set_board_size(size):
        global board_size
        board_size = size
        puzzle.board_size = size
        utils.board_size = size
        backtracking.board_size = size
        Generic.board_size = size
        create_gui(root, frame)  # Create the Sudoku GUI

    label = tk.Label(frame, text="Select Sudoku Board Size", font=("Arial", 14))
    label.pack(pady=10)

    button_4x4 = tk.Button(frame, text="4x4", font=("Arial", 12), command=lambda: set_board_size(4))
    button_4x4.pack(pady=5)

    button_9x9 = tk.Button(frame, text="9x9", font=("Arial", 12), command=lambda: set_board_size(9))
    button_9x9.pack(pady=5)

    button_16x16 = tk.Button(frame, text="16x16", font=("Arial", 12), command=lambda: set_board_size(16))
    button_16x16.pack(pady=5)

def create_gui(root, frame):
    """Main Sudoku GUI."""
    for widget in frame.winfo_children():
        widget.destroy()

    def update_gui(arr):
        """Update the GUI with the current board state."""
        for i in range(board_size):
            for j in range(board_size):
                entries[i][j].delete(0, tk.END)
                if arr[i][j] != 0:
                    entries[i][j].insert(tk.END, arr[i][j])
        root.update_idletasks()

    def solve_and_display():
        """Solve the Sudoku and display the solution."""
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

        Generic.INITIAL_SUDOKU = [row.copy() for row in grid]

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

        def run_genetic_solver():
            solution = genetic_algorithm(
                Generic.INITIAL_SUDOKU,
                progress_callback=lambda grid: update_gui(grid),
            )
            if fitness(solution) == 0:
                update_gui(solution)
                messagebox.showinfo("Success", "Sudoku Solved using Genetic Algorithm!")
            else:
                messagebox.showerror("Error", "Failed to solve the Sudoku.")

        if use_generic_solver.get():
            threading.Thread(target=run_genetic_solver, daemon=True).start()
        else:
            empty_cells = [(row, col) for row in range(board_size) for col in range(board_size) if grid[row][col] == 0]
            SL = []
            NSL = [(empty_cells[0], 0, [])]
            DE = []
            backtracking.solve_sudoku_async(grid, empty_cells, SL, NSL, DE, update_gui, root)

    def generate_random_and_display():
        """Generate and display a random Sudoku puzzle."""
        grid = generate_random_sudoku()
        for i in range(board_size):
            for j in range(board_size):
                entries[i][j].delete(0, tk.END)
                if grid[i][j] != 0:
                    entries[i][j].insert(tk.END, grid[i][j])

    def reset_grid():
        """Reset the grid to an empty state."""
        for i in range(board_size):
            for j in range(board_size):
                entries[i][j].delete(0, tk.END)

    def hint_and_display():
        """Provide a hint for the next move."""
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

    entries = create_board_entries(frame, board_size)

    button_frame = tk.Frame(frame)
    button_frame.grid(row=board_size, column=0, columnspan=board_size, pady=10)

    use_generic_solver = tk.BooleanVar()
    use_generic_solver.set(False)

    def toggle_solver():
        use_generic_solver.set(not use_generic_solver.get())
        toggle_solver_button.config(
            text="Switch to Original Solver" if use_generic_solver.get() else "Switch to Genetic Solver"
        )

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

# Main execution
root = tk.Tk()
root.title("Sudoku Solver")
main_frame = tk.Frame(root)
main_frame.pack(pady=20, padx=20)

show_board_size_selection_window(root, main_frame)
root.mainloop()
