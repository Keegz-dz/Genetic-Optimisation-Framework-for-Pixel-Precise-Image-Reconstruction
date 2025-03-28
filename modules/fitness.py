"""
This module provides functions to calculate fitness scores for individuals in the population.
The primary fitness measure is based on the difference between the target image and the candidate solution.
Additional functions for diversity and entropy-based fitness can be used to incorporate more complex criteria.
"""

import numpy as np
from scipy import stats


def fitness_fun(target_chrom, indiv_chrom):
    """
    Calculate the fitness of an individual solution based on the mean absolute difference.
    
    A lower mean absolute difference indicates a closer match to the target image.
    To align with maximization convention, the fitness is computed as the sum of target values minus this difference.
    
    Parameters:
        target_chrom (np.array): Flattened target image.
        indiv_chrom (np.array): Flattened candidate solution.
    
    Returns:
        float: The computed fitness score (higher is better).
    """
    fitness = np.mean(np.abs(target_chrom - indiv_chrom))
    fitness = np.sum(target_chrom) - fitness                # Invert difference: a lower difference leads to a higher fitness value.
    
    return fitness


def calc_population_fitness(target_chrom, population):
    """
    Compute the fitness scores for each individual in the population.
    
    Parameters:
        target_chrom (np.array): Flattened target image.
        population (np.array): Array of candidate solutions.
    
    Returns:
        np.array: An array of fitness scores corresponding to each individual.
    """
    quality = np.zeros(population.shape[0])
    for indv_num in range(population.shape[0]):
        quality[indv_num] = fitness_fun(target_chrom, population[indv_num, :])
        
    return quality


def diversity_fitness_fun(target_chrom, indiv_chrom, population):
    """
    Calculate a diversity-adjusted fitness score that penalizes similarity to other individuals.
    
    This function first computes the mean absolute difference from the target image, then
    subtracts a penalty based on the average Euclidean distance (similarity) of the candidate
    to all other individuals in the population.
    
    Parameters:
        target_chrom (np.array): Flattened target image.
        indiv_chrom (np.array): Flattened candidate solution.
        population (np.array): Full population of candidate solutions.
    
    Returns:
        float: The diversity-adjusted fitness score.
    """
    fitness = np.mean(np.abs(target_chrom - indiv_chrom))       
    
    # Compute similarity penalty: average norm difference between candidate and every individual.
    similarity_penalty = np.mean(np.linalg.norm(population - indiv_chrom, axis=1))
    
    return fitness - 0.1 * similarity_penalty

def calc_population_diversity_fitness(target_chrom, population):
    """
    Compute diversity-adjusted fitness scores for the entire population.
    
    Parameters:
        target_chrom (np.array): Flattened target image.
        population (np.array): Array of candidate solutions.
    
    Returns:
        np.array: An array of diversity-adjusted fitness scores.
    """
    quality = np.zeros(population.shape[0])     # Initialize fitness scores
    
    # Calculate fitness for each individual in the population using the diversity function
    for indv_num in range(population.shape[0]):
        quality[indv_num] = diversity_fitness_fun(target_chrom, population[indv_num, :], population)
        
    return quality


def entropy_fitness_fun(target_chrom, indiv_chrom):
    """
    Calculate an entropy-adjusted fitness score for a candidate solution.
    
    This function computes the mean absolute difference and can incorporate the entropy of the candidate
    to reward solutions with a desirable level of complexity or randomness.
    
    Parameters:
        target_chrom (np.array): Flattened target image.
        indiv_chrom (np.array): Flattened candidate solution.
    
    Returns:
        float: The entropy-adjusted fitness score.
    """
    fitness = np.mean(np.abs(target_chrom - indiv_chrom))
    
    # !Uncomment the following lines if using entropy in the fitness calculation
    # indiv_entropy = stats.entropy(indiv_chrom.flatten(), base=2)
    # fitness = fitness - 0.01 * indiv_entropy
    
    return fitness

def calc_population_entropy_fitness(target_chrom, population):
    """
    Compute entropy-adjusted fitness scores for the entire population.
    
    Parameters:
        target_chrom (np.array): Flattened target image.
        population (np.array): Array of candidate solutions.
    
    Returns:
        np.array: An array of entropy-adjusted fitness scores.
    """
    quality = np.zeros(population.shape[0])
    
    for indv_num in range(population.shape[0]):
        quality[indv_num] = entropy_fitness_fun(target_chrom, population[indv_num, :])
        
    return quality
