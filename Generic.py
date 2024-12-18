import random

# Global board size and sub-box size
global board_size  # Adjustable based on the GUI selection


# Default initial Sudoku grid
global INITIAL_SUDOKU

def make_gene(row):
    """Create a shuffled row while respecting fixed cells."""
    gene = list(range(1, board_size + 1))
    random.shuffle(gene)
    for i, val in enumerate(row):
        if val != 0:
            gene.remove(val)
            gene.insert(i, val)
    return gene

def make_chromosome(grid):
    """Create a full Sudoku board as a chromosome."""
    return [make_gene(row) for row in grid]

def make_population(count, grid):
    """Generate an initial population."""
    return [make_chromosome(grid) for _ in range(count)]

def fitness(chromosome):
    """Calculate conflicts in rows, columns, and boxes."""
    conflicts = 0

    # Row conflicts
    for row in chromosome:
        conflicts += board_size - len(set(row))

    # Column conflicts
    for col in range(board_size):
        col_values = [chromosome[row][col] for row in range(board_size)]
        conflicts += board_size - len(set(col_values))

    box_size = int(board_size ** 0.5)
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
    """Swap two mutable cells within a row with a given probability."""
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
        # Keep fixed cells from INITIAL_SUDOKU
        for i in range(board_size):
            if INITIAL_SUDOKU[parent1.index(row1)][i] != 0:
                child_row[i] = row1[i]
        child.append(child_row)
    return child

def tournament_selection(population, k=5):
    """Select the best individual from k random solutions."""
    selected = random.sample(population, k)
    return min(selected, key=fitness)

def genetic_algorithm(initial_grid, population_size=1200, generations=1200, mutation_prob=0.2, progress_callback=None):
    """Run the genetic algorithm to solve Sudoku."""
    population = make_population(population_size, initial_grid)
    best_solution = min(population, key=fitness)
    best_score = fitness(best_solution)

    for generation in range(generations):
        next_population = []

        # Elitism: Keep the best solution
        next_population.append(best_solution)

        # Generate the rest of the population
        for _ in range(population_size - 1):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = crossover(parent1, parent2)
            next_population.append(mutation(child, mutation_prob))

        population = next_population
        current_best = min(population, key=fitness)
        current_score = fitness(current_best)

        # Update the best solution
        if current_score < best_score:
            best_solution, best_score = current_best, current_score

        # Update the GUI in real-time
        if progress_callback:
            progress_callback(current_best)

        # Stop if fitness = 0
        if best_score == 0:
            print(f"Perfect solution found at generation {generation}")
            return best_solution

        # Print progress every 100 generations
        if generation % 100 == 0:
            print(f"Generation {generation}: Best Fitness = {best_score}")

    print("No perfect solution found within the given generations.")
    return best_solution
