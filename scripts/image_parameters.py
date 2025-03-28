"""
This module is responsible for processing an input image file and extracting key parameters
required for the genetic algorithm. It reads the image, converts it into a NumPy array, and
generates essential data including the original image (as a PIL Image), the array representation,
the shape of the image, and the flattened array (chromosome) that represents the image.
It also resizes every input image to speed up the genetic algorithm.
"""

import numpy as np
from PIL import Image


def Main(image_path):
    """
    Read the image from the provided path, resize it to 100x100 pixels, and extract image parameters.

    Parameters:
        image_path (str): The file path to the target image.

    Returns:
        list: A list containing:
            - target_img (PIL Image): The original image.
            - target_arr (np.array): The image represented as a NumPy array.
            - img_shape (tuple): The dimensions (shape) of the image.
            - target_chromosome (np.array): A flattened version of the image array.
    """
    target_img = Image.open(image_path)
    target_img = target_img.resize((150, 150))
    target_img = target_img.convert("RGB")      # Ensure the image is in RGB format
    target_arr = np.array(target_img)           # Convert the image to a NumPy array
    img_shape = target_arr.shape                # (height, width, channels)
    target_chromosome = target_arr.flatten()    # Flatten the image array to create a 1D "chromosome" representation
    
    parameters_list = [target_img, target_arr, img_shape, target_chromosome]
    
    return parameters_list

if __name__ == "__main__":
    image_path = "data/raw/fruit.jpg"
    parameters_list = Main(image_path)
    
    # Unpack the returned parameters for demonstration purposes
    target_img, target_arr, img_shape, target_chromosome = parameters_list
    
    print("target_img:", target_img)
    print("img_shape:", img_shape)
    print("target_chromosome:", target_chromosome)
    print("target_arr:", target_arr)
