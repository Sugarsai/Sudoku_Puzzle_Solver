import math

global board_size

def used_in_row(arr, row, num):
    for i in range(board_size):
        if arr[row][i] == num:
            return True
    return False


def used_in_col(arr, col, num):
    for i in range(board_size):
        if arr[i][col] == num:
            return True
    return False


def used_in_box(arr, row, col, num):
    for i in range(int(math.sqrt(board_size))):
        for j in range(int(math.sqrt(board_size))): # iterates at every cell of the 3x3 subgrid
            if arr[i + row][j + col] == num:
                return True
    return False


def check_location_is_safe(arr, row, col, num):
    return (not used_in_row(arr, row, num) and
            not used_in_col(arr, col, num) and
            not used_in_box(arr, row - (row % int(math.sqrt(board_size))), col - (col % int(math.sqrt(board_size))), num))

# row - row % 3 => getting the first row index of its 3x3 subgrid
# col - col % 3 => same but for row