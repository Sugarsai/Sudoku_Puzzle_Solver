import time
from logging import root

from utils import check_location_is_safe
global board_size

def solve_sudoku_async(arr, empty_cells, SL, NSL, DE, update_gui, root, delay=0):
    if len(SL) == len(empty_cells):  # Base case: solved
        update_gui(arr)
        return True

    if NSL:
        CS, last_num, tried_nums = NSL.pop()
        row, col = CS

        for num in range(last_num + 1, board_size + 1):
            if num not in tried_nums and check_location_is_safe(arr, row, col, num):
                arr[row][col] = num
                SL.append(CS)
                NSL.append((CS, num, tried_nums + [num]))
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
                update_gui(arr)
                root.after(delay, lambda: solve_sudoku_async(arr, empty_cells, SL, NSL, DE, update_gui, root, delay))
                return True
    return False
