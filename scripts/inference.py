"""
This is the main entry point for the Genetic Optimization for Pixel-Precise Image Reconstruction project.
It loads image parameters from Modules/image_parameters.py, runs the genetic algorithm from model/genetic_model.py,
saves the final image in the output folder (data/processed), and displays the final generated image.
"""

import os
import sys
import matplotlib.pyplot as plt
from PIL import Image
import shutil

# Adjust sys.path so that the project root is included.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..")
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import image_parameters  # noqa: E402
from model import genetic_model  # noqa: E402


def clear_checkpoint_directory(checkpoint_dir):
    """
    Remove all files from the checkpoint directory.
    """
    if os.path.exists(checkpoint_dir):
        shutil.rmtree(checkpoint_dir)
    os.makedirs(checkpoint_dir, exist_ok=True)


def display_side_by_side(original_path, final_path):
    """
    Display the original input image (resized to 150x150) alongside the final generated image.
    
    Parameters:
        original_path (str): Path to the original input image.
        final_path (str): Path to the final generated image.
    
    Returns:
        None
    """
    # Load and resize the original image to 150x150.
    original_img = Image.open(original_path)
    original_img_resized = original_img.resize((150, 150))
    
    # Load the final generated image.
    final_img = Image.open(final_path)
    
    # Create a side-by-side comparison plot.
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].imshow(original_img_resized)
    axes[0].set_title("Original (150x150)")
    axes[0].axis("off")
    
    axes[1].imshow(final_img)
    axes[1].set_title("Final Generated Image")
    axes[1].axis("off")
    
    plt.tight_layout()
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
    # Clear previous checkpoints.
    checkpoint_dir = os.path.join(output_folder, "checkpoint")
    if os.path.exists(checkpoint_dir):
        clear_checkpoint_directory(checkpoint_dir)
    else:
        os.makedirs(checkpoint_dir, exist_ok=True)
    
    # Load image parameters.
    parameters_list = image_parameters.Main(image_path)
    # Run the genetic algorithm.
    genetic_model.genetic_algorithm(parameters_list, output_folder)
    
    # Define the final image path.
    final_image_path = os.path.join(output_folder, "solution.png")
    if display:
        display_side_by_side(image_path, final_image_path)

if __name__ == "__main__":
    inference(
        image_path="data/raw/test.png",
        output_folder="data/processed",
        display=True
    )
