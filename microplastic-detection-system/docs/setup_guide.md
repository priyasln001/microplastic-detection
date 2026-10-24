# Step-by-Step Setup Guide

## 1. Environment Setup
Install Python 3.8+ and the following libraries:
- `pip install flask flask-cors ultralytics opencv-python requests`

## 2. Running the Backend
- Navigate to the `backend/` folder.
- Run `python app.py`.
- The server will automatically download `yolov8n.pt` on the first run.

## 3. Launching the UI
- Double-click `frontend/index.html`.
- Ensure the backend is running; otherwise, the "Analyze" button will show an error.

## 4. Hardware Integration (Raspberry Pi)
- Connect a Pi HQ Camera or USB Webcam.
- Run `python hardware/raspberry_pi.py`.
- It will capture a frame every 10 seconds and send it to the backend for remote processing.

## 5. Training your own Model
- Place your labeled dataset in the `dataset/` folder.
- Configure `data.yaml`.
- Run `python ml-model/train.py`.
