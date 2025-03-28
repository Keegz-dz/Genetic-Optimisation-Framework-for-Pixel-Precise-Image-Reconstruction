"""
This module implements crossover functions to combine parent chromosomes and generate offspring.
It provides two strategies:
  - Single-point crossover: Splits chromosomes at the midpoint.
  - Multi-point crossover: Uses two random crossover points to mix genetic material from three parents.
Each function takes the selected parent chromosomes and produces a new population of candidate solutions.
"""

import numpy as np
import itertools
import random

def single_pt_crossover(parents, img_shape, individual_count):
    """
    Generate a new population using single-point crossover.

    In this strategy, each offspring is created by combining the first half of one parent's chromosome
    with the second half of another parent's chromosome.

    Parameters:
        parents (np.array): 2D array of selected parent chromosomes.
        img_shape (tuple): The shape of the target image (used to determine chromosome length).
        individual_count (int): Total number of individuals to generate in the new population.

    Returns:
        np.array: New population of candidate solutions after applying single-point crossover.
    """
    # Calculate total number of elements (pixels) per chromosome.
    num_elements = np.prod(img_shape)
    new_population = np.empty((individual_count, num_elements), dtype=np.uint8)
    
    new_population[0:parents.shape[0], :] = parents                                 # Copy the parent chromosomes into the new population.
    num_newly_generated = individual_count - parents.shape[0]                       # Calculate how many offspring need to be generated.
    parents_permutations = list(itertools.permutations(range(parents.shape[0]), 2)) # Generate all possible pairs of parents.
    
    # Shuffle the order of these permutations.
    permutation_indices = list(range(len(parents_permutations)))
    random.shuffle(permutation_indices)
    selected_permutations = permutation_indices[:num_newly_generated]
    
    comb_indx = parents.shape[0]    # Start index for placing new offspring in the population.
    
    for comb in range(len(selected_permutations)):
        selected_comb_indx = selected_permutations[comb]
        selected_comb = parents_permutations[selected_comb_indx]
        
        # Determine the midpoint for the crossover.
        half_size = np.int32(new_population.shape[1] / 2)
        
        # Create offspring by combining halves of the selected parents.
        new_population[comb_indx + comb, 0:half_size] = parents[selected_comb[0], 0:half_size]  # First half from first parent
        new_population[comb_indx + comb, half_size:] = parents[selected_comb[1], half_size:]    # Second half from second parent
    
    return new_population

def multi_pt_crossover(parents, img_shape, individual_count):
    """
    Generate a new population using multi-point crossover.

    In this strategy, three parents are randomly selected for each offspring. Two random crossover points
    are chosen, and the offspring's chromosome is created by:
      - Taking genes up to the first crossover point from the first parent,
      - Genes between the first and second crossover points from the second parent,
      - And the remaining genes from the third parent.

    Parameters:
        parents (np.array): 2D array of selected parent chromosomes.
        img_shape (tuple): The shape of the target image (used to determine chromosome length).
        individual_count (int): Total number of individuals to generate in the new population.

    Returns:
        np.array: New population of candidate solutions after applying multi-point crossover.
    """
    # Calculate total number of elements per chromosome.
    num_elements = np.prod(img_shape)
    new_population = np.empty((individual_count, num_elements), dtype=np.uint8)
    
    # Copy parent chromosomes into the new population.
    new_population[0:parents.shape[0], :] = parents
    
    # Calculate how many offspring need to be generated.
    num_newly_generated = individual_count - parents.shape[0]
    
    for i in range(num_newly_generated):
        # Randomly select three distinct parents for the crossover.
        selected_parents = random.sample(range(parents.shape[0]), 3)
        selected_parents.sort()  # Sorting is optional and only for consistency
        
        # Choose two random crossover points.
        crossover_points = [random.randint(0, num_elements) for _ in range(2)]
        crossover_points.sort()  # Ensure the first point is less than the second
        
        # Create offspring by combining segments from the three selected parents.
        new_population[parents.shape[0] + i, :crossover_points[0]] = \
            parents[selected_parents[0], :crossover_points[0]]
        
        new_population[parents.shape[0] + i, crossover_points[0]:crossover_points[1]] = \
            parents[selected_parents[1], crossover_points[0]:crossover_points[1]]
        
        new_population[parents.shape[0] + i, crossover_points[1]:] = \
            parents[selected_parents[2], crossover_points[1]:]
    
    return new_population
