"""
This module handles the initialization of the population and performs consistency checks
for the genetic algorithm. It generates an initial set of candidate solutions (each represented
as a flattened image) and ensures that the chosen number of parents is sufficient for generating
the required number of offspring.
"""

import numpy as np
import itertools


def initial_population(img_shape, individual_count=8, dtype=np.uint8):
    """
    Generate a random initial population of candidate solutions.

    Parameters:
        img_shape (tuple): The dimensions (shape) of the target image.
        individual_count (int): Number of candidate solutions (individuals) in the population.
        dtype (data-type): Data type for the population array (default is np.uint8).

    Returns:
        np.array: A 2D NumPy array where each row represents a flattened image (chromosome).
    """
    # Calculate the total number of pixels in the image.
    total_pixels = np.prod(img_shape)
    
    # Generate a random population with pixel values in the range [0, 255].
    init_population = np.random.randint(0, 256, size=(individual_count, total_pixels), dtype=dtype)
    
    return init_population


def check_sufficient_parents(num_parents_mating, sol_per_population):
    """
    Check if the chosen number of parents is sufficient for generating the required offspring.

    This function calculates the number of unique parent pairs (order matters) and
    compares it with the number of offspring needed. This helps prevent configuration
    errors in the genetic algorithm.

    Parameters:
        num_parents_mating (int): Number of parents selected for mating.
        sol_per_population (int): Total number of candidate solutions in the population.

    Returns:
        bool: True if there are enough unique parent permutations to generate the required offspring,
              False otherwise.
    """
    num_possible_permutations = len(list(itertools.permutations(range(num_parents_mating), 2)))     # Calculate the number of unique parent pairs (order matters)
    num_required_permutations = sol_per_population - num_possible_permutations                      # Determine the number of additional offspring needed beyond the available permutations.
   
    return num_required_permutations <= num_possible_permutations
