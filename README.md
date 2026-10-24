# Smart Multi-Environment Microplastic Detection System

This repository contains the code and documentation for a comprehensive, AI-powered system designed to detect and analyze microplastics across various environmental samples (water, solid waste, sludge).

## 🚀 Features
- **Modular Design:** Separate analysis modules for Water, Solid Waste, and Sludge.
- **AI-Powered Detection:** Integrates YOLOv8 for object detection and classification of microplastics (fibers, fragments, beads).
- **Interactive UI:** Built with Streamlit for a user-friendly research dashboard.
- **Hardware Ready:** Designed to interface with Raspberry Pi HQ cameras, UV LEDs, and automated logic circuits.

## 📁 Repository Structure
```
project_root/
├── app.py                      # Main Streamlit dashboard
├── pages/                      # Streamlit modules
│   ├── 1_💧_Water_Analysis.py
│   ├── 2_🗑️_Solid_Waste_Analysis.py
│   └── 3_🧪_Sludge_Analysis.py
├── scripts/                    # ML and Setup scripts
│   ├── prepare_dataset.py      # Script to initialize YOLOv8 folder structure
│   └── train_model.py          # Script to run YOLOv8 training
├── data/                       # Datasets
│   └── microplastics_dataset/  # Configured by prepare_dataset.py
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🛠️ Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Installation
Clone the repository and install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Running the Dashboard
Launch the intelligent web dashboard using Streamlit:
```bash
streamlit run app.py
```
This will open the interface in your web browser where you can interact with the mock inference models and upload generated images.

### 4. Training the AI Model (YOLOv8)
If you want to train the object detection model on real data:

1. **Prepare Data Structure:**
   ```bash
   python scripts/prepare_dataset.py
   ```
2. **Add Data:** Place your labeled images (YOLO `.txt` format) into `data/microplastics_dataset/train/images` and `../labels`.
3. **Train:**
   ```bash
   python scripts/train_model.py
   ```
## 🔬 AI Model Details
The system targets using **YOLOv8** due to its state-of-the-art speed and accuracy for real-time edge devices (like Jetson Nano or Raspberry Pi). It classifies particles into three primary categories:
- `fiber`
- `fragment`
- `bead`

## ⚙️ Hardware Recommendations
For real-world deployment, this software stack integrates with:
1.  **Compute:** Raspberry Pi 4/5 or NVIDIA Jetson Nano.
2.  **Optics:** Raspberry Pi HQ Camera or Digital USB Microscope.
3.  **Lighting:** Switchable White LED Ring & 365nm UV LED (for fluorescence).
4.  **Sensors:** IR Breakbeam (for waste conveyor).
