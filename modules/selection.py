"""
This module contains functions for selecting the best individuals (parents) from the population
based on their fitness scores. The selected parents are used for the mating process in the genetic algorith
"""

import numpy as np

def selecting_mating_pool(num_parents, population, quality):
    """
    Select the top individuals as parents for mating based on fitness scores.

    Parameters:
        num_parents (int): Number of parents to select.
        population (np.array): Array of individuals.
        quality (np.array): Fitness scores for each individual.

    Returns:
        np.array: Selected parents.
    """
    parents = np.empty((num_parents, population.shape[1]), dtype=np.uint8)
    
    for parent_num in range(num_parents):
        max_indx = np.where(quality == np.max(quality))[0][0]    # Find the index of the individual with the highest fitness score.
        parents[parent_num, :] = population[max_indx, :]         # Assign the best candidate to the parents array. 
        quality[max_indx] = -1                                   # Prevent reselection
        
    return parents
