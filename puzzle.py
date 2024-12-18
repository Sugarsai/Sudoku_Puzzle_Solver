from utils import check_location_is_safe
import random
global board_size

def generate_random_sudoku():
    grid = [[0 for _ in range(board_size)] for _ in range(board_size)] # fills the 9x9 grid with zeros
    for _ in range(board_size-1): # عدد القيم الراندوم اللي هتتحط
        row, col = random.randint(0, board_size-1), random.randint(0, board_size-1) #chooses a randow cell to be filled
        num = random.randint(1, board_size)
        if check_location_is_safe(grid, row, col, num):
            grid[row][col] = num
    return grid

def get_hint(grid):
    for row in range(board_size):
        for col in range(board_size):
            if grid[row][col] == 0:
                for num in range(1, board_size - 1):  # see that any num between 1 and 9 is safe
                    if check_location_is_safe(grid, row, col, num):
                        return (row, col, num)
    return None