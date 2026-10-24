import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import sys

# Add project root to path to import src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.core.model_utils import MicroplasticDetector
from src.core.hardware import HardwareController

st.set_page_config(page_title="Water Analysis", page_icon="💧", layout="wide")

# --- Initialize Singleton Instances ---
if 'detector' not in st.session_state:
    # Use standard yolov8n weights for demo
    st.session_state.detector = MicroplasticDetector('yolov8n.pt') 
if 'hw' not in st.session_state:
    st.session_state.hw = HardwareController()

st.title("💧 Water Microplastic Detection")
st.markdown("Automated detection in water samples using **Nile Red Fluorescence (365nm)**.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("System Control")
    mode = st.radio("Active Optic Channel", ["White LED (Standard)", "UV 365nm (Fluorescence)"])
    use_uv = mode == "UV 365nm (Fluorescence)"
    
    # Update Hardware State
    if st.button("Apply Lighting Configuration"):
        light_mode = 'uv' if use_uv else 'white'
        st.session_state.hw.set_lighting(light_mode)
        st.success(f"Hardware updated: {mode}")

    st.divider()
    
    source = st.selectbox("Image Source", ["Upload File", "Real-time Hardware Capture"])
    
    upload_file = None
    if source == "Upload File":
        upload_file = st.file_uploader("Upload Micrograph", type=['jpg', 'jpeg', 'png'])
    else:
        if st.button("📸 Capture from Microscope"):
            with st.spinner("Capturing..."):
                 cap_path = st.session_state.hw.capture_image('water_cap.jpg')
                 if cap_path:
                     upload_file = 'water_cap.jpg'
                 else:
                     st.error("Hardware capture failed.")

with col2:
    st.subheader("AI Analytics Engine")
    if upload_file:
        # Load image
        if isinstance(upload_file, str):
            image = cv2.imread(upload_file)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_pil = Image.open(upload_file)
            image = np.array(image_pil)
            if len(image.shape) == 2: # Grayscale
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            elif image.shape[2] == 4: # RGBA
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

        st.image(image, caption="Current View", use_column_width=True)
        
        conf = st.slider("Detection Confidence Threshold", 0.1, 1.0, 0.25)
        
        if st.button("🚀 Execute Detection Pipeline", type="primary"):
             with st.spinner("Processing Frame..."):
                 res_img, count, types = st.session_state.detector.predict(image, conf_threshold=conf)
                 
                 st.image(res_img, caption="AI Identification Overlay (YOLOv8)", channels="RGB", use_column_width=True)
                 
                 st.success(f"Analysis Complete! {count} particles detected.")
                 
                 # Metrics
                 m1, m2, m3, m4 = st.columns(4)
                 m1.metric("Total Count", count)
                 m2.metric("Fragments", types.get('fragment', 0))
                 m3.metric("Fibers", types.get('fiber', 0))
                 m4.metric("Beads", types.get('bead', 0))
                 
                 # Export
                 csv_content = f"timestamp,total_count,fibers,fragments,beads\n{time.time()},{count},{types.get('fiber',0)},{types.get('fragment',0)},{types.get('bead',0)}"
                 st.download_button("📥 Export Research Data (CSV)", data=csv_content, file_name="water_report.csv")
    else:
        st.info("Please provide a sample image to start the AI analysis.")

import time # For the CSV timestamp
