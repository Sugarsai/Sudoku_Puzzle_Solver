import random

# Global board size and sub-box size
global board_size
global INITIAL_SUDOKU

def make_gene(row):
    """Create a shuffled row while respecting fixed cells."""
    fixed_positions = {i: val for i, val in enumerate(row) if val != 0}
    available_numbers = set(range(1, board_size + 1)) - set(fixed_positions.values())
    gene = [0] * board_size
    
    # Place fixed numbers first
    for pos, val in fixed_positions.items():
        gene[pos] = val
    
    # Fill remaining positions
    available_positions = [i for i in range(board_size) if i not in fixed_positions]
    available_numbers = list(available_numbers)
    random.shuffle(available_numbers)
    
    for pos, num in zip(available_positions, available_numbers):
        gene[pos] = num
    
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
    box_size = int(board_size ** 0.5)

    # Column conflicts
    for col in range(board_size):
        column = [chromosome[row][col] for row in range(board_size)]
        conflicts += len(column) - len(set(column))

    # Box conflicts
    for box_row in range(0, board_size, box_size):
        for box_col in range(0, board_size, box_size):
            box = []
            for i in range(box_size):
                for j in range(box_size):
                    box.append(chromosome[box_row + i][box_col + j])
            conflicts += len(box) - len(set(box))

    return conflicts

def repair_chromosome(chromosome):
    """Repair invalid chromosomes to maintain Sudoku constraints."""
    for i in range(board_size):
        fixed_positions = {j: val for j, val in enumerate(INITIAL_SUDOKU[i]) if val != 0}
        row = chromosome[i]
        
        # Check for duplicates in non-fixed positions
        numbers = list(range(1, board_size + 1))
        used_numbers = set(fixed_positions.values())
        available_numbers = [n for n in numbers if n not in used_numbers]
        
        # Get positions that need fixing
        non_fixed_positions = [j for j in range(board_size) if j not in fixed_positions]
        current_values = [row[j] for j in non_fixed_positions]
        
        # Fix duplicates
        if len(set(current_values)) != len(current_values):
            random.shuffle(available_numbers)
            for pos, num in zip(non_fixed_positions, available_numbers):
                row[pos] = num
                
    return chromosome

def mutation(chromosome, probability):
    """Enhanced mutation that swaps two mutable cells within a row."""
    mutated = [row[:] for row in chromosome]
    
    for i in range(board_size):
        if random.random() < probability:
            mutable_indices = [j for j in range(board_size) if INITIAL_SUDOKU[i][j] == 0]
            if len(mutable_indices) > 1:
                idx1, idx2 = random.sample(mutable_indices, 2)
                mutated[i][idx1], mutated[i][idx2] = mutated[i][idx2], mutated[i][idx1]
    
    return repair_chromosome(mutated)

def crossover(parent1, parent2):
    """Improved crossover with repair mechanism."""
    child = []
    for i, (row1, row2) in enumerate(zip(parent1, parent2)):
        fixed_positions = {j: val for j, val in enumerate(INITIAL_SUDOKU[i]) if val != 0}
        
        # Create child row
        if random.random() < 0.5:
            child_row = row1[:]
        else:
            child_row = row2[:]
            
        # Ensure fixed positions are maintained
        for pos, val in fixed_positions.items():
            child_row[pos] = val
            
        child.append(child_row)
    
    return repair_chromosome(child)

def tournament_selection(population, k=5):
    """Select the best individual from k random solutions."""
    tournament = random.sample(population, k)
    return min(tournament, key=fitness)

def genetic_algorithm(initial_grid, population_size=7000, generations=1200, mutation_prob=0.2, progress_callback=None):
    """Run the genetic algorithm to solve Sudoku."""
    global INITIAL_SUDOKU
    INITIAL_SUDOKU = initial_grid
    
    # Initialize population
    population = make_population(population_size, initial_grid)
    population = [repair_chromosome(chrom) for chrom in population]
    
    best_solution = min(population, key=fitness)
    best_score = fitness(best_solution)
    
    stagnation_counter = 0
    last_best_score = best_score

    for generation in range(generations):
        # Create next generation
        next_population = []
        
        # Elitism: Keep the best 10% solutions
        elite_size = max(1, population_size // 10)
        sorted_population = sorted(population, key=fitness)
        next_population.extend(sorted_population[:elite_size])
        
        # Generate rest of the population
        while len(next_population) < population_size:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = crossover(parent1, parent2)
            child = mutation(child, mutation_prob)
            next_population.append(child)
        
        population = next_population
        current_best = min(population, key=fitness)
        current_score = fitness(current_best)
        
        # Update best solution
        if current_score < best_score:
            best_solution = current_best
            best_score = current_score
            stagnation_counter = 0
        else:
            stagnation_counter += 1
        
        # Adaptive mutation rate
        if stagnation_counter > 20:
            mutation_prob = min(0.8, mutation_prob * 1.1)
        else:
            mutation_prob = max(0.1, mutation_prob * 0.9)
        
        # Update GUI
        if progress_callback:
            progress_callback(current_best)
        
        # Early stopping condition
        if best_score == 0:
            print(f"Perfect solution found at generation {generation}")
            return best_solution
            
        # Print progress
        if generation % 100 == 0:
            print(f"Generation {generation}: Best Fitness = {best_score}, Mutation Rate = {mutation_prob:.3f}")
    
    print("No perfect solution found within the given generations.")
    return best_solution