import streamlit as st

st.set_page_config(
    page_title="Microplastic Detection System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔬 Smart Multi-Environment Microplastic Detection System")

st.markdown("""
Welcome to the research-level Microplastic Detection System. This platform integrates advanced hardware optics, robotics, and machine learning to detect, classify, and quantify microplastics across multiple environments.

### 🌐 System Modules
Select a module from the sidebar to begin analysis:

#### 1. 💧 Water Analysis (Core Module)
Detects microplastics in water samples using high-resolution microscopy and membrane filtration. Supports UV/Fluorescence mode for enhanced detection (e.g., Nile Red staining).

#### 2. 🗑️ Solid Waste / Dustbin Analysis
Analyzes macro plastics and potential microplastic sources in solid waste using RGB/IR triggers and advanced ML (classification of PET, HDPE, etc.).

#### 3. 🧪 Moist / Sludge Analysis
Handles complex, noisy environments like sludge. Includes preprocessing and robust AI segmentation for detection against chaotic backgrounds.

---
**Powered by:** YOLOv8, PyTorch, OpenCV, and Raspberry Pi / Jetson Nano.
""")

st.info("👈 Please select an analysis module from the sidebar to continue.")

st.sidebar.success("Select a module above.")

# Global Dashboard Stats Mockup
st.divider()
st.subheader("Global Environmental Pollution Metrics (Mock)")
col1, col2, col3 = st.columns(3)
col1.metric(label="Total Particles Detected (Today)", value="1,245", delta="12% from yesterday", delta_color="inverse")
col2.metric(label="High Risk Zones Detected", value="3", delta="1 new", delta_color="inverse")
col3.metric(label="Overall System Accuracy", value="94.2%", delta="Optimal", delta_color="normal")
