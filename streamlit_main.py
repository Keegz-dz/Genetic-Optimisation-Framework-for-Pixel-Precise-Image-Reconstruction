import streamlit as st
st.set_page_config(page_title="Genetic Image Reconstruction", layout="wide")

import cv2              # noqa: E402
import numpy as np      # noqa: E402
import tempfile         # noqa: E402
import os               # noqa: E402
import threading        # noqa: E402
import time             # noqa: E402
from PIL import Image   # noqa: E402
import shutil           # noqa: E402 

# Import the necessary modules from your project.
from scripts import image_parameters  # noqa: E402
from model import genetic_model       # noqa: E402

# --- Inject Custom CSS ---
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
    2. Click "Reconstruct" to start the genetic algorithm.
    3. Watch as checkpoint images from this run are generated and displayed.
    4. Once finished, the final image is shown along with a gallery of checkpoints.
    """
)

# --- Helper Functions ---

def resize_for_display(image, max_width=500):
    """
    Resize an image (BGR or RGB) for display if its width exceeds max_width.
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
    files.sort(key=lambda x: int(x.replace("checkpoint_", "").replace(".png", "")))
    full_paths = [os.path.join(checkpoint_dir, f) for f in files]
    return full_paths

def run_genetic_algorithm(input_path, output_folder):
    """
    Run the genetic algorithm inference.
    This function is designed to run in a separate thread.
    """
    parameters_list = image_parameters.Main(input_path)
    genetic_model.genetic_algorithm(parameters_list, output_folder)

def clear_checkpoint_directory(checkpoint_dir):
    """
    Remove all files from the checkpoint directory.
    """
    if os.path.exists(checkpoint_dir):
        shutil.rmtree(checkpoint_dir)
    os.makedirs(checkpoint_dir, exist_ok=True)

# --- Main App Content ---

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], key="image_upload")

if uploaded_file is not None:
    # Save the uploaded file to a temporary file.
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    tfile.close()
    
    # Read the image using OpenCV.
    image = cv2.imread(tfile.name)
    
    if image is None:
        st.error("Error loading the image. Please try another file.")
    else:
        image_for_display = resize_for_display(image)
        with st.expander("Preview Uploaded Image"):
            st.image(cv2.cvtColor(image_for_display, cv2.COLOR_BGR2RGB), caption="Original Low-Resolution Image", use_container_width=True)
        
        # Define output folder and checkpoint directory.
        output_folder = "data/processed"
        checkpoint_dir = os.path.join(output_folder, "checkpoint")
        os.makedirs(output_folder, exist_ok=True)
        os.makedirs(checkpoint_dir, exist_ok=True)
        
        # Clear any previous checkpoints to avoid mixing runs.
        clear_checkpoint_directory(checkpoint_dir)
        
        if st.button("Reconstruct"):
            # Run genetic algorithm in a separate thread.
            ga_thread = threading.Thread(target=run_genetic_algorithm, args=(tfile.name, output_folder))
            ga_thread.start()
            
            progress_placeholder = st.empty()
            checkpoint_placeholder = st.empty()
            st.info("Processing image. Please wait while checkpoints are generated...")
            
            # Poll the checkpoint folder periodically.
            while ga_thread.is_alive():
                checkpoints = load_checkpoint_images(checkpoint_dir)
                if checkpoints:
                    latest_checkpoint = checkpoints[-1]
                    checkpoint_placeholder.image(
                        Image.open(latest_checkpoint),
                        width=150,
                        caption=f"Latest Checkpoint: {os.path.basename(latest_checkpoint)}",
                        use_container_width=False
                    )
                progress_placeholder.text("Processing... (checkpoints will update as they are generated)")
                time.sleep(2)
            
            ga_thread.join()
            progress_placeholder.text("Processing complete!")
            
            final_image_path = os.path.join(output_folder, "solution.png")
            st.success("Genetic algorithm finished. Final image:")
            st.image(Image.open(final_image_path), use_container_width=True, caption="Final Generated Image")
            
            # --- Display Checkpoint Gallery in a 3-Column Grid ---
            st.markdown("### Checkpoint Gallery")
            checkpoint_files = load_checkpoint_images(checkpoint_dir)
            if checkpoint_files:
                # Display images in rows of 3.
                for i in range(0, len(checkpoint_files), 3):
                    cols = st.columns(3)
                    for j, cp in enumerate(checkpoint_files[i:i+3]):
                        with cols[j]:
                            st.image(
                                Image.open(cp),
                                width=150,
                                caption=os.path.basename(cp),
                                use_container_width=False
                            )
    
    os.remove(tfile.name)
