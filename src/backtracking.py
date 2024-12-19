from utils import check_location_is_safe
import matplotlib.pyplot as plt
global board_size

# Initialize global variables for statistics
steps = []
cells_solved = []
backtracking_steps = []

def plot_statistics():
    # Plot the cells solved over time
    plt.figure(figsize=(10, 6))
    plt.plot(steps, cells_solved, label="Cells Solved", color="green")
    plt.xlabel("Step Number")
    plt.ylabel("Cells Solved")
    plt.title("Cells Solved Over Time")
    plt.legend()
    plt.grid()

    # Plot the backtracking steps over time
    plt.twinx()  # Overlay the plot
    plt.plot(steps, backtracking_steps, label="Backtracking Count", color="red", linestyle="--")
    plt.ylabel("Backtracking Steps")
    plt.legend(loc="upper left")

    plt.show()

def solve_sudoku_async(arr, empty_cells, SL, NSL, DE, update_gui, root, delay=0):
    if len(SL) == len(empty_cells):  # Base case: solved
        print(f"Sudoku solved! Steps taken: {len(SL)}")
        update_gui(arr)
        plot_statistics()  # Plot the data once solved
        return True

    if NSL:
        CS, last_num, tried_nums = NSL.pop()
        row, col = CS
        print(f"Trying cell ({row}, {col}). Previously tried numbers: {tried_nums}")

        for num in range(last_num + 1, board_size + 1):
            if num not in tried_nums and check_location_is_safe(arr, row, col, num):
                arr[row][col] = num
                SL.append(CS)
                NSL.append((CS, num, tried_nums + [num]))
                print(f"Placed {num} in cell ({row}, {col}). Cells solved: {len(SL)}/{len(empty_cells)}")

                # Update statistics
                steps.append(len(steps) + 1)
                cells_solved.append(len(SL))
                backtracking_steps.append(len(DE))

                update_gui(arr)

                if len(SL) < len(empty_cells):
                    next_cell = empty_cells[len(SL)]
                    NSL.append((next_cell, 0, []))

                # Schedule the next step after a delay
                root.after(delay, lambda: solve_sudoku_async(arr, empty_cells, SL, NSL, DE, update_gui, root, delay))
                return True
        else:
            # Backtrack if no valid numbers
            if SL:
                DE.append(SL.pop())
                arr[row][col] = 0
                print(f"Backtracking from cell ({row}, {col}). Backtracks so far: {len(DE)}")

                # Update statistics
                steps.append(len(steps) + 1)
                cells_solved.append(len(SL))
                backtracking_steps.append(len(DE))

                update_gui(arr)
                root.after(delay, lambda: solve_sudoku_async(arr, empty_cells, SL, NSL, DE, update_gui, root, delay))
                return True
    return False
