"""
This module orchestrates the overall genetic algorithm process for image regeneration.
It integrates population initialization, fitness evaluation, selection, crossover, mutation,
and saving of checkpoint images as well as the final best performing image.
"""

import sys
import os
from tqdm import tqdm
import numpy as np

# Adjust sys.path so that the project root is included.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..")
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from modules import population, fitness, selection, crossover, mutation  # noqa: E402
from model.helpers import saving  # noqa: E402

def genetic_algorithm(parameters_list, folderPath, generations=300000, save_point=20000):
    """
    Run the genetic algorithm to regenerate an image based on the target parameters.

    The process includes:
      1. Population Initialization
      2. Fitness Evaluation
      3. Selection of best individuals (parents)
      4. Offspring generation via multi-point crossover
      5. Enhanced mutation to introduce variability
      6. Saving checkpoint images at regular intervals and final image output

    Parameters:
        parameters_list (list): Contains [target_img, target_arr, img_shape, target_chromosome].
        folderPath (str): Directory where the final output image will be saved.
        generations (int): Number of generations to run the algorithm.
        save_point (int): Interval (in generations) at which to save checkpoint images.

    Returns:
        None
    """
    sol_per_population = 8    # Total number of individuals in the population
    num_parents_mating = 4    # Number of parents selected for mating
    mutation_percent = 0.01   # Percentage of genes to mutate

    target_img, target_arr, img_shape, target_chromosome = parameters_list

    # Check configuration for sufficient parent permutations.
    if not population.check_sufficient_parents(num_parents_mating, sol_per_population):
        print("\n*Inconsistency in the selected population size or number of parents.*")
        sys.exit(1)

    # Initialize a random population.
    new_population = population.initial_population(img_shape, sol_per_population)

    # Create a checkpoint folder inside the output folder.
    checkpoint_folder = os.path.join(folderPath, "checkpoint")
    if not os.path.exists(checkpoint_folder):
        os.makedirs(checkpoint_folder)

    for generation in tqdm(range(generations), desc="Running Genetic Algorithm"):
        
        # Evaluate fitness for each individual.
        fit_quality = fitness.calc_population_fitness(target_chromosome, new_population)
        
        # Select top individuals as parents.
        parents = selection.selecting_mating_pool(num_parents_mating, new_population, fit_quality)
        
        # Generate offspring via multi-point crossover.
        new_population = crossover.multi_pt_crossover(parents, img_shape, sol_per_population)
        new_population = mutation.enhanced_mutation(new_population, num_parents_mating, mutation_percent)

        # Save checkpoint images at regular intervals (except generation 0).
        if generation % save_point == 0 and generation != 0:
            checkpoint_file = os.path.join(checkpoint_folder, f"checkpoint_{generation}.png")
            saving.save_images(generation, fit_quality, new_population, img_shape, save_point, checkpoint_folder, filename=checkpoint_file)
    
    # Save the final image as solution.png in the output folder.
    final_file = os.path.join(folderPath, "solution.png")
    best_solution_chrom = new_population[np.where(fit_quality == np.max(fit_quality))[0][0], :]
    best_solution_img = saving.chromosome2img(best_solution_chrom, img_shape)
    from matplotlib import pyplot as plt  
    plt.imsave(final_file, best_solution_img)
