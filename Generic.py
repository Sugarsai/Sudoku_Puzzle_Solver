import random

# Global board size
board_size = 4  # Supports 4x4, 9x9, 16x16 Sudoku
box_size = int(board_size ** 0.5)

# INITIAL_SUDOKU = [
#     [0, 0, 0, 0, 0, 0, 0, 0, 8],
#     [0, 0, 3, 0, 0, 2, 0, 0, 0],
#     [0, 0, 0, 4, 8, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 6],
#     [0, 0, 0, 8, 0, 4, 0, 0, 0],
#     [7, 5, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 9, 3, 0, 0, 0],
#     [0, 0, 0, 6, 0, 0, 4, 0, 0],
#     [9, 0, 0, 0, 0, 0, 0, 0, 0],
# ]

INITIAL_SUDOKU = [
    [0, 0, 0, 0],
    [0, 0, 3, 0],
    [0, 0, 0, 4],
    [0, 0, 0, 0],
]

# Utility Functions
def make_gene(row):
    """Create a shuffled row with respect to fixed cells."""
    gene = list(range(1, board_size + 1))
    random.shuffle(gene)
    for i, val in enumerate(row):
        if val != 0:
            gene.remove(val)
            gene.insert(i, val)
    return gene

def make_chromosome(grid):
    """Create a complete chromosome (board) respecting fixed cells."""
    return [make_gene(row) for row in grid]

def make_population(count, grid):
    """Generate the initial population."""
    return [make_chromosome(grid) for _ in range(count)]

def fitness(chromosome):
    """Calculate fitness based on conflicts in rows, columns, and boxes."""
    conflicts = 0

    # Row conflicts
    for row in chromosome:
        conflicts += board_size - len(set(row))

    # Column conflicts
    for col in range(board_size):
        col_values = [chromosome[row][col] for row in range(board_size)]
        conflicts += board_size - len(set(col_values))

    # Box conflicts
    for box_row in range(0, board_size, box_size):
        for box_col in range(0, board_size, box_size):
            box_values = [
                chromosome[i][j]
                for i in range(box_row, box_row + box_size)
                for j in range(box_col, box_col + box_size)
            ]
            conflicts += board_size - len(set(box_values))

    return conflicts

def mutation(chromosome, probability):
    """Swap two mutable cells within a row."""
    for i in range(board_size):
        if random.random() < probability:
            mutable_indices = [j for j in range(board_size) if INITIAL_SUDOKU[i][j] == 0]
            if len(mutable_indices) > 1:
                idx1, idx2 = random.sample(mutable_indices, 2)
                chromosome[i][idx1], chromosome[i][idx2] = chromosome[i][idx2], chromosome[i][idx1]
    return chromosome

def crossover(parent1, parent2):
    """Perform two-point crossover."""
    child = []
    for row1, row2 in zip(parent1, parent2):
        point1, point2 = sorted(random.sample(range(board_size), 2))
        child_row = row1[:point1] + row2[point1:point2] + row1[point2:]
        child.append([
            row1[i] if INITIAL_SUDOKU[parent1.index(row1)][i] != 0 else child_row[i]
            for i in range(board_size)
        ])
    return child

def tournament_selection(population, k=5):
    """Select the best individual out of k random choices."""
    selected = random.sample(population, k)
    return min(selected, key=fitness)

def genetic_algorithm(initial_grid, population_size=400, generations=4000, mutation_prob=0.1, progress_callback=None):
    """Run the genetic algorithm with GUI updates."""
    population = make_population(population_size, initial_grid)
    best_solution = min(population, key=fitness)
    best_score = fitness(best_solution)

    for generation in range(generations):
        next_population = []

        for _ in range(population_size):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = crossover(parent1, parent2)
            next_population.append(mutation(child, mutation_prob))

        population = next_population
        current_best = min(population, key=fitness)
        current_score = fitness(current_best)

        # Update the best solution if a better one is found
        if current_score < best_score:
            best_solution, best_score = current_best, current_score

        # Update GUI every generation using the callback
        if progress_callback:
            progress_callback(current_best)

        # Stop if a perfect solution is found
        if best_score == 0:
            print(f"Solution found at generation {generation}")
            return best_solution

        # Print progress every 500 generations
        if generation % 500 == 0:
            print(f"Generation {generation}: Best Fitness = {best_score}")

    print("No perfect solution found.")
    return best_solution
