import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import threading
import time
from PIL import Image

# Import the necessary modules from your project.
from .modules import image_parameters
from model import genetic_model

# Set page configuration and custom CSS.
st.set_page_config(page_title="Genetic Image Reconstruction", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background-color: #e8f4f8;
        font-size: 14px;
    }
    .stButton>button {
        background-color: #0066cc;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px 24px;
        border: none;
    }
    h1 {
        text-align: center;
        color: #003366;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Genetic Optimization for Pixel-Precise Image Reconstruction")
st.sidebar.title("Instructions")
st.sidebar.info(
    """
    **Steps:**
    1. Upload a low-resolution image.
    2. Click "Enhance Image" to start the genetic algorithm.
    3. Watch as checkpoint images are generated and displayed.
    4. Once finished, the final image is shown.
    """
)

# --- Helper Functions ---

def resize_for_display(image, max_width=500):
    """
    Resize an image (in BGR or RGB format) for display if its width exceeds max_width.
    """
    height, width = image.shape[:2]
    if width > max_width:
        ratio = max_width / width
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return image

def load_checkpoint_images(checkpoint_dir):
    """
    Retrieve and sort checkpoint image file paths from the checkpoint directory.
    Returns the sorted list (by generation number).
    """
    if not os.path.exists(checkpoint_dir):
        return []
    files = [f for f in os.listdir(checkpoint_dir) if f.startswith("checkpoint_") and f.endswith(".png")]
    # Sort files by the integer in the filename.
    files.sort(key=lambda x: int(x.replace("checkpoint_", "").replace(".png", "")))
    full_paths = [os.path.join(checkpoint_dir, f) for f in files]
    return full_paths

def display_checkpoint(image_path):
    """
    Display a checkpoint image using Streamlit.
    """
    img = Image.open(image_path)
    st.image(img, use_column_width=True)

def run_genetic_algorithm(input_path, output_folder):
    """
    Run the genetic algorithm inference.
    This function is designed to run in a separate thread.
    """
    # Load image parameters from the uploaded image.
    parameters_list = image_parameters.Main(input_path)
    # Run the genetic algorithm; this function will save checkpoint images and final image.
    genetic_model.genetic_algorithm(parameters_list, output_folder)

# --- Main App Logic ---

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save the uploaded file to a temporary file.
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    tfile.close()
    
    # Read image using OpenCV.
    image = cv2.imread(tfile.name)
    
    if image is None:
        st.error("Error loading the image. Please try another file.")
    else:
        # Resize image for preview.
        image_for_display = resize_for_display(image)
        
        with st.expander("Preview Uploaded Image"):
            st.image(cv2.cvtColor(image_for_display, cv2.COLOR_BGR2RGB), caption="Original Low-Resolution Image", use_column_width=True)
        
        # Define output folder and checkpoint directory.
        output_folder = "data/processed"
        checkpoint_dir = os.path.join(output_folder, "checkpoint")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
        
        if st.button("Enhance Image"):
            # Start genetic algorithm in a separate thread.
            ga_thread = threading.Thread(target=run_genetic_algorithm, args=(tfile.name, output_folder))
            ga_thread.start()
            
            # Display a loading spinner and progress area.
            progress_placeholder = st.empty()
            checkpoint_placeholder = st.empty()
            
            st.info("Processing image. Please wait while checkpoints are generated...")
            # Poll the checkpoint folder periodically until the genetic algorithm thread finishes.
            while ga_thread.is_alive():
                # Get the current list of checkpoint images.
                checkpoints = load_checkpoint_images(checkpoint_dir)
                if checkpoints:
                    # Display the latest checkpoint image.
                    latest_checkpoint = checkpoints[-1]
                    checkpoint_placeholder.image(Image.open(latest_checkpoint), caption=f"Checkpoint: {os.path.basename(latest_checkpoint)}", use_column_width=True)
                # Update a progress message (you could also use st.progress if you have an estimated total)
                progress_placeholder.text("Processing... (checkpoints will update as they are generated)")
                time.sleep(2)
            
            ga_thread.join()
            progress_placeholder.text("Processing complete!")
            
            # Display the final generated image.
            final_image_path = os.path.join(output_folder, "solution.png")
            st.success("Genetic algorithm finished. Final image:")
            st.image(Image.open(final_image_path), caption="Final Generated Image", use_column_width=True)
            
            # Optionally, display a gallery of all checkpoints.
            st.markdown("### Checkpoint Gallery")
            checkpoint_files = load_checkpoint_images(checkpoint_dir)
            if checkpoint_files:
                cols = st.columns(3)
                for i, cp in enumerate(checkpoint_files):
                    with cols[i % 3]:
                        st.image(Image.open(cp), caption=os.path.basename(cp), use_column_width=True)
            
    # Clean up temporary file.
    os.remove(tfile.name)
