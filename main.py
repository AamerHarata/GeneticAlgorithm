import random
import numpy as np
import functions as f
import objects as o

# Try to create 100 generations of 16 vertices
# generations = []

total_nodes = 16
total_generations = 100
total_initial_population = 100

population = []

# Create initial population (parents)
initial_population = [f.create_chromosome(total_nodes) for _ in range(total_initial_population)]
population.extend(initial_population)

# Create children of n generations
generations = f.create_N_generations(initial_population, total_generations)
population.extend(generations)

# Eliminate half of population
population = f.eliminate_n_chromosomes(population)

# Search mutations
population.extend(f.create_mutations(population))

# Remove possible duplications
population = f.remove_duplications(population)

# Create graphs
graphs = [o.Graph(x) for x in population]

# Get the best solution
best_graph = f.best_n_solutions(graphs, 1)[0]

# Plot the best solution
f.plot_solution(best_graph)

# print solution
best_graph.Print()
