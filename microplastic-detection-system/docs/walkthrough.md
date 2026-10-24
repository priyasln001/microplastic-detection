# 🔬 Microplastic AI Detection System - User Guide

Your frontend is now fully operational and significantly upgraded! I've integrated it directly with the Flask backend to provide a seamless "single-service" experience.

## 🚀 How to Launch
1. Ensure your backend is running. If not, run:
   ```bash
   cd backend
   python app.py
   ```
2. Open your browser and navigate to:
   [**http://localhost:5000**](http://localhost:5000)

---

## ✨ Features & Upgrades

### 1. Premium Visual Dashboard
The UI has been redesigned with a modern dark theme, glassmorphism effects, and real-time status indicators. It now looks and feels like a research-grade laboratory tool.

### 2. Live vision & Analysis
- **🎥 Start Real-Time Feed**: Automatically connects to your webcam and runs YOLOv8 + contour filtering on every frame.
- **🔴 Live Indicator**: A pulsing indicator appears when the stream is active.
- **📊 Real-Time Analytics**: Watch the particle count and classification tags update dynamically as the AI scans the feed.

### 3. Static Sample Analysis
- **📁 Upload**: Click "Choose Sample Image" and select a file.
- **⚡ Processing**: The system highlights detected plastics with bounding boxes and classifies them as **Fiber**, **Fragment**, or **Bead**.
- **✅ Status**: Instantly see if a sample is "SAFE" or "PLASTIC DETECTED".

### 4. System Logs
The new **System Logs** panel at the bottom right tracks backend communication, and analysis results, making it much easier to monitor system health.

---

## 🧪 Testing Samples
I have generated and added two research-grade sample images for you to test the detection system immediately:
- `dataset/sample_images/sample1.png` (Fibers & Fragments)
- `dataset/sample_images/sample2.png` (Micro-beads)

Try uploading these to see the AI in action!

---

## 🛠️ Technical Fixes Applied
- **Backend-Served Frontend**: Flask now serves `index.html`, eliminating CORS issues and making it easier to host.
- **Dynamic URL Discovery**: The JS now automatically detects if it's being served from localhost or a different IP.
- **Robust Error Handling**: Added logging for fetch failures and clearer alerts for backend connectivity issues.
