import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import random

st.set_page_config(page_title="Sludge Analysis", page_icon="🧪", layout="wide")

st.title("🧪 Moist / Sludge Microplastic Detection")
st.markdown("Analyze complex sludge samples post-thermal drying. Uses enhanced robust segmentation for noisy backgrounds.")

def mock_sludge_detection(image):
    # Simulate processing with specific sludge algorithms
    progress_text = "Applying Adaptive Filtering and Background Subtraction..."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.015)
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.empty()

    img_np = np.array(image)
    if len(img_np.shape) == 2:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_GRAY2RGB)
    elif img_np.shape[2] == 4:
         img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)

    h, w, _ = img_np.shape
    
    # Generate random blobs imitating microplastics in sludge
    num_particles = random.randint(10, 40)
    
    # Create an overlay for segmentation masks
    overlay = img_np.copy()
    
    for _ in range(num_particles):
        x = random.randint(20, w - 20)
        y = random.randint(20, h - 20)
        radius = random.randint(3, 15)
        
        # High contrast colors for visibility against dark sludge
        color = random.choice([(0, 255, 255), (255, 0, 255), (0, 255, 0)]) 
        
        # Draw filled circle for mask
        cv2.circle(overlay, (x, y), radius, color, -1)
        # Draw contour
        cv2.circle(img_np, (x, y), radius, (255, 255, 255), 1)

    # Blend overlay with original
    alpha = 0.5
    cv2.addWeighted(overlay, alpha, img_np, 1 - alpha, 0, img_np)

    return img_np, num_particles

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Sample Preparation")
    st.write("**Pre-requisite:** Sample must be dried using heating plate and chemical digestion (e.g., Fenton's reagent or KOH) if heavy organic matter is present.")
    
    st.markdown("---")
    upload_file = st.file_uploader("Upload Sludge Micrograph", type=['jpg', 'jpeg', 'png'])
    
    st.subheader("Advanced Filtering")
    denoise = st.slider("Denoising Strength (Non-Local Means)", 1, 10, 5)
    contrast = st.slider("Contrast Enhancement (CLAHE)", 1.0, 5.0, 2.5)

with col2:
    st.subheader("Segmented View")
    if upload_file is not None:
        image = Image.open(upload_file)
        st.image(image, caption="Raw Sludge Sample", use_column_width=True)
        
        if st.button("🔬 Process & Segment Image", type="primary"):
            res_img, count = mock_sludge_detection(image)
            st.image(res_img, caption="AI Segmented Particles against Sludge Matrix", channels="RGB", use_column_width=True)
            
            st.metric("Estimated Microplastic Load", f"{count} particles / mg")
            st.info("The segmentation masks (cyan/magenta) denote areas of high polymer probability within the organic matrix.")
    else:
        st.info("Upload treated sludge micrograph to begin.")
