"""
This module provides mutation functions to introduce random variations in the offspring.
It includes three mutation techniques:
  1. Basic Mutation: Randomly changes a subset of genes in the offspring.
  2. Enhanced Mutation: Applies color adjustments and non-uniform changes to the genes.
  3. Brush Stroke Mutation: Simulates a brush stroke effect by replacing a continuous segment of genes.
Each function operates on the population array, leaving the best-performing parents unchanged.
"""

import numpy as np
import random

def mutation(population, num_parents_mating, mut_percent):
    """
    Apply basic mutation to the population by randomly changing a subset of genes.
    
    This function randomly selects a set of gene indices in each offspring (excluding the parents)
    and assigns new random values between 0 and 255 to those genes.
    
    Parameters:
        population (np.array): 2D array where each row is a candidate solution (flattened image).
        num_parents_mating (int): Number of top individuals (parents) that are not subject to mutation.
        mut_percent (float): Percentage of genes (pixels) to mutate in each offspring.
    
    Returns:
        np.array: The mutated population.
    """
    # Loop through each offspring (skipping the parent individuals)
    for indx in range(num_parents_mating, population.shape[0]):
        # Determine the number of genes to mutate based on the mutation percentage.
        num_genes = population.shape[1]
        num_mutations = np.uint32(mut_percent/100 * num_genes)
        
        # Select random indices to mutate.
        rand_indx = np.uint32(np.random.random(size=num_mutations) * num_genes)
        
        # Generate new random values for the selected genes.
        new_values = np.uint8(np.random.random(size=rand_indx.shape[0]) * 256)
        
        # Apply the mutations.
        population[indx, rand_indx] = new_values
        
    return population


def enhanced_mutation(population, num_parents_mating, mut_percent):
    """
    Apply enhanced mutation that includes color adjustments and non-uniform mutations.
    
    In addition to randomly selecting genes to mutate, this function:
      - Adjusts gene values slightly to simulate subtle color mutations.
      - Applies a non-uniform mutation by scaling gene values with a random strength.
      - Uses clipping to ensure that gene values remain within the valid range (0 to 255).
    
    Parameters:
        population (np.array): 2D array of candidate solutions.
        num_parents_mating (int): Number of parent individuals not subject to mutation.
        mut_percent (float): Percentage of genes (pixels) to mutate in each offspring.
    
    Returns:
        np.array: The population after applying enhanced mutation.
    """
    for indx in range(num_parents_mating, population.shape[0]):
        num_genes = population.shape[1]
        num_mutations = np.uint32(mut_percent/100 * num_genes)
        
        # Randomly select gene indices to mutate.
        rand_indx = np.uint32(np.random.random(size=num_mutations) * num_genes)
        
        # Color mutation: adjust gene values by adding a random value between -20 and 20.
        population[indx, rand_indx] += np.uint8(np.random.randint(-20, 20, size=rand_indx.shape[0]))
        population[indx, rand_indx] = np.clip(population[indx, rand_indx], 0, 255)
        
        # Non-uniform mutation: further adjust the gene values based on a random mutation strength.
        mutation_strength = np.random.random(size=rand_indx.shape[0]) * 2.0 - 1.0  # Random values between -1 and 1
        population[indx, rand_indx] += np.uint8(mutation_strength * population[indx, rand_indx])
        population[indx, rand_indx] = np.clip(population[indx, rand_indx], 0, 255)
        
    return population


def brush_stroke_mutation(population, num_parents_mating, mut_percent, brush_stroke_size):
    """
    Apply mutation that simulates brush strokes on the image.
    
    This function works similarly to enhanced mutation, with an additional step:
      - A continuous segment of genes (simulating a brush stroke) is replaced by random pixel values.
    
    Parameters:
        population (np.array): 2D array of candidate solutions.
        num_parents_mating (int): Number of parent individuals not subject to mutation.
        mut_percent (float): Percentage of genes to mutate in each offspring.
        brush_stroke_size (int): The size (number of genes) of the brush stroke effect.
    
    Returns:
        np.array: The population after applying brush stroke mutation.
    """
    for indx in range(num_parents_mating, population.shape[0]):
        num_genes = population.shape[1]
        num_mutations = np.uint32(mut_percent/100 * num_genes)
        
        # Randomly select gene indices for mutation.
        rand_indx = np.uint32(np.random.random(size=num_mutations) * num_genes)
        
        # Apply basic and non-uniform mutations as in enhanced_mutation.
        population[indx, rand_indx] += np.uint8(np.random.randint(-20, 20, size=rand_indx.shape[0]))
        population[indx, rand_indx] = np.clip(population[indx, rand_indx], 0, 255)
        
        mutation_strength = np.random.random(size=rand_indx.shape[0]) * 2.0 - 1.0
        population[indx, rand_indx] += np.uint8(mutation_strength * population[indx, rand_indx])
        population[indx, rand_indx] = np.clip(population[indx, rand_indx], 0, 255)
        
        # Simulate a brush stroke: replace a continuous segment with random values.
        brush_start = np.random.randint(0, num_genes - brush_stroke_size)
        brush_end = brush_start + brush_stroke_size
        population[indx, brush_start:brush_end] = np.uint8(np.random.randint(0, 256, size=brush_stroke_size))
        
    return population
