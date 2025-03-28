"""
This is the main entry point for the Genetic Optimization for Pixel-Precise Image Reconstruction project.
It loads image parameters from Modules/image_parameters.py, runs the genetic algorithm from model/genetic_model.py,
saves the final image in the output folder (data/processed), and displays the final generated image.
"""

import os
import sys
import matplotlib.pyplot as plt
from PIL import Image

# Adjust sys.path so that the project root is included.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..")
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import image_parameters  # noqa: E402
from model import genetic_model  # noqa: E402

def display_image(image_path):
    """
    Display the image located at the given path using matplotlib.
    
    Parameters:
        image_path (str): Path to the image file.
    
    Returns:
        None
    """
    img = Image.open(image_path)
    plt.figure(figsize=(8, 6))
    plt.imshow(img)
    plt.axis("off")
    plt.title("Final Generated Image")
    plt.show()

def inference(image_path="data/raw/fruit.jpg", output_folder="data/processed", display=True):
    """
    Run the genetic algorithm to regenerate an image, save the final output,
    and display the final generated image.
    
    Parameters:
        image_path (str): Path to the input image.
        output_folder (str): Directory where the final image will be saved.
        display (bool): If True, display the final output image.
    
    Returns:
        None
    """
    # Load image parameters (target image, array representation, image shape, flattened chromosome).
    parameters_list = image_parameters.Main(image_path)
    # Run the genetic algorithm.
    genetic_model.genetic_algorithm(parameters_list, output_folder)
    # Define the final image path.
    final_image_path = os.path.join(output_folder, "solution.png")
    # Display the final image.
    if display:
        display_image(final_image_path)

if __name__ == "__main__":
    inference(
        image_path="data/raw/test.jpg",
        output_folder="data/processed",
        display=True
    )
