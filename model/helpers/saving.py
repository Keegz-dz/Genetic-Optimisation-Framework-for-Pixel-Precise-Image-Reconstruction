"""
This module provides functionality for saving the best-performing candidate image
from the genetic algorithm process. It converts a flattened chromosome back to the 
original image shape and saves it as an image file. An optional filename parameter 
allows for custom naming (useful for checkpoint images).
"""

import os
import numpy as np
from matplotlib import pyplot as plt

def chromosome2img(chromosome, im_shape):
    """
    Convert a 1D chromosome (flattened image) back to its original image shape.
    
    Parameters:
        chromosome (np.array): Flattened image array.
        im_shape (tuple): Original dimensions of the image.
    
    Returns:
        np.array: Reshaped image array.
    """
    return np.reshape(chromosome, im_shape)

def save_images(curr_iteration, qualities, new_population, im_shape, save_point, save_dir, filename=None):
    """
    Save the best solution of the current generation as an image file.
    
    At every generation that is a multiple of save_point, the function selects the individual 
    with the highest fitness from the population, converts it back to image format, and saves it.
    
    Parameters:
        curr_iteration (int): Current generation number.
        qualities (np.array): Fitness scores for the current generation.
        new_population (np.array): Array containing candidate solutions.
        im_shape (tuple): Original shape of the image.
        save_point (int): Interval (in generations) at which images are saved.
        save_dir (str): Directory where the image will be saved.
        filename (str, optional): Custom filename for saving the image. If not provided,
                                  the image is saved as "solution.png" in save_dir.
    
    Returns:
        None
    """
    if np.mod(curr_iteration, save_point) == 0:
        best_solution_chrom = new_population[np.where(qualities == np.max(qualities))[0][0], :]
        best_solution_img = chromosome2img(best_solution_chrom, im_shape)
        if filename is None:
            filename = os.path.join(save_dir, "solution.png")
        plt.imsave(filename, best_solution_img)
