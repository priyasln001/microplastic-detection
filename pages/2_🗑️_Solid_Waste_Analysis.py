import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import random

st.set_page_config(page_title="Solid Waste Analysis", page_icon="🗑️", layout="wide")

st.title("🗑️ Solid Waste / Dustbin Analysis")
st.markdown("Analyze macroscopic solid waste to classify plastics and identify degradation (sources of microplastics).")

def mock_waste_detection(image):
    # Simulate processing
    progress_text = "Running CNN Classification on Waste Items..."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.empty()

    img_np = np.array(image)
    if len(img_np.shape) == 2:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_GRAY2RGB)
    elif img_np.shape[2] == 4:
         img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)

    h, w, _ = img_np.shape
    
    # Draw a large bounding box for the main object
    x1, y1 = int(w*0.1), int(h*0.1)
    x2, y2 = int(w*0.9), int(h*0.9)
    
    cv2.rectangle(img_np, (x1, y1), (x2, y2), (255, 165, 0), 4) # Orange box
    
    plastic_types = ["PET (Polyethylene Terephthalate)", "HDPE (High-Density Polyethylene)", "Non-Plastic", "LDPE (Low-Density Polyethylene)"]
    detected_type = random.choice(plastic_types)
    degradation_level = random.choice(["Low", "Medium", "High (High risk of microplastic shedding)"])
    
    label = f"{detected_type}"
    cv2.putText(img_np, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 165, 0), 2)

    return img_np, detected_type, degradation_level

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Conveyor / IR Trigger")
    auto_trigger = st.toggle("Enable IR Sensor Auto-Trigger")
    if auto_trigger:
        st.info("🟢 Monitoring... Waiting for objects to pass sensor.")
    
    upload_file = st.file_uploader("Upload Image of Waste Item", type=['jpg', 'jpeg', 'png'])

with col2:
    st.subheader("Object Analysis")
    if upload_file is not None:
        image = Image.open(upload_file)
        st.image(image, caption="Current Item on Conveyor", use_column_width=True)
        
        if st.button("🔍 Identify Plastic Type", type="primary"):
            res_img, plastic_type, degradation = mock_waste_detection(image)
            st.image(res_img, caption="Classification Result", channels="RGB", use_column_width=True)
            
            st.subheader("Detailed Breakdown")
            st.write(f"**Material Detected:** {plastic_type}")
            if "Non-Plastic" in plastic_type:
                st.success("Safe material detected.")
            else:
                 if "High risk" in degradation:
                     st.error(f"**Degradation Level:** {degradation}")
                 elif "Medium" in degradation:
                     st.warning(f"**Degradation Level:** {degradation}")
                 else:
                     st.info(f"**Degradation Level:** {degradation}")
                 
                 st.progress(random.randint(10, 90), text="Environmental Microplastic Generation Risk Index")
    else:
        st.info("Waiting for input...")
