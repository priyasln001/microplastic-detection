# Production-Level Implementation & Execution Guide

This document provides a complete, no-missing-components walkthrough for deploying the Smart Microplastic Detection System.

---

## Phase 1: Physical Assembly
### 1.1 Optical Darkroom
- Construct a light-proof enclosure (15x15x20 cm).
- Mount the Pi HQ Camera/Lens on the top ceiling facing down.
- Install the dual-channel relay to control:
   - Channel 1: 365nm UV LED strip.
   - Channel 2: White LED ring light.
- Place the membrane filter stage 10-15cm below the lens (adjust for focus).

### 1.2 Conveyor Hardware (Module 2)
- Align the IR Transmitter and Receiver across the belt.
- Connect IR OUT to Pi GPIO 22.
- Ensure the belt motor is powered independently to avoid electrical noise in the AI feed.

---

## Phase 2: Software Environment Setup
Execute in your terminal (PowerShell/Bash):

### 2.1 Dependency Installation
```bash
# Core Requirements
pip install ultralytics streamlit opencv-python RPi.GPIO pandas pillow
```

### 2.2 Dataset Initialization
To train the system on YOUR specific microplastics (essential for high accuracy):
1. Place raw microscope images in `data/microplastics_dataset/train/images`.
2. Annotate them using [Roboflow](https://roboflow.com) or [LabelImg](https://github.com/HumanSignal/labelImg) (YOLO format).
3. Run the preparation script:
   ```bash
   python scripts/prepare_dataset.py
   ```
4. Start training:
   ```bash
   python scripts/train_model.py
   ```

---

## Phase 3: System Execution
### 3.1 Local Development / Simulation Mode
Run without RPi hardware (uses webcam and mock GPIO log):
```bash
streamlit run app.py
```

### 3.2 Field Deployment (Raspberry Pi/Jetson)
1. Set up the hardware as per `docs/Hardware_Circuit_Diagram.md`.
2. Connect to the Pi via SSH.
3. Launch the dashboard:
   ```bash
   python -m streamlit run app.py --server.address 0.0.0.0
   ```
4. Access the dashboard from any device on the network via `http://<pi_ip_address>:8501`.

---

## Phase 4: Workflow for Water Sample Analysis
1. **Filtration:** Vacuum filter 1L of water through a 0.45µm GF/F membrane.
2. **Staining:** Apply 1mL of Nile Red (10µg/mL) to the filter; wait 15 mins.
3. **Capture:** In the Dashboard, select "UV 365nm" and "Hardware Capture".
4. **Quantify:** The AI automatically highlights particles and generates a CSV report.

## Phase 5: Environmental Risk Assessment (Sludge)
1. **Preprocessing:** Ensure `src/core/model_utils.py` is configured with `yolov8-seg.pt` for segmentation.
2. **Analysis:** Review the overlap between organic material (grey) and detections (colored masks).
3. **Index:** Use the "Environmental Risk Index" on Page 3 to determine total pollutant concentration per gram of sample.

---

**System Integrity Check:**
- [x] Hardware Core Created (src/core/hardware.py)
- [x] AI Engine Operational (src/core/model_utils.py)
- [x] Multi-Environment Interface (pages/)
- [x] Circuit / Doc Assets (docs/)
