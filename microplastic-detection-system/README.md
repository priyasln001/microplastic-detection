# Smart Microplastic Detection System (Hardware + AI)

A full-stack, research-level application for detecting, quantifying, and classifying microplastics (fibers, fragments, beads) across multiple environments.

## 📁 Project Structure
- `backend/`: Flask API with YOLOv8 integration.
- `frontend/`: Web Dashboard (HTML/CSS/JS).
- `ml-model/`: Training and detection scripts.
- `hardware/`: Raspberry Pi / Camera integration scripts.
- `dataset/`: Sample images for testing.
- `docs/`: Setup guide and project documentation.

## 🚀 Getting Started

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Wait for the message: `Running on http://0.0.0.0:5000`

### 2. Frontend Setup
- Simply open `frontend/index.html` in your web browser.
- Or use a Live Server (VS Code extension).

### 3. Usage
1. Click **"Analyze Image"** to upload a sample from `dataset/sample_images/`.
2. View the highlighted microplastics and the count analytics.

## ⚙️ Hardware Simulation
To simulate a Raspberry Pi capturing and sending data:
```bash
cd hardware
python raspberry_pi.py
```

## 🧪 AI Model Details
The system uses **YOLOv8** for real-time object detection.
- **Classes**: Fiber, Fragment, Bead.
- **Accuracy**: Targeting >90% mAP on microscopic samples.

## 🔬 Research Significance
Automates the tedious process of manual microscopic counting using machine vision, allowing for continuous environmental monitoring in water treatment plants and sludge analysis.
