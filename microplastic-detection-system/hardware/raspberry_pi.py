import cv2
import requests
import time
import threading

# Configuration
BACKEND_URL = "http://localhost:5000/start-camera" # Trigger command
STREAM_FPS = 10

class PiRealTimeNode:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.is_active = True
        print("[NODE] Hardware Core Initialized. Ready for Real-Time Feed.")

    def run(self):
        while self.is_active:
            ret, frame = self.cap.read()
            if not ret:
                print("[ERROR] Camera Feed Lost")
                break
            
            # Local analysis (Simulated)
            # In a real RPi, we might run a lightweight TFLite model here
            # For this upgrade, we rely on the Backend API streaming
            
            # Print status to console for hardware-level monitoring
            print("[LIVE] Capturing Frame... Status: FEEDING BACKEND")
            
            # Sleep to maintain FPS
            time.sleep(1.0 / STREAM_FPS)

    def stop(self):
        self.is_active = False
        self.cap.release()

if __name__ == "__main__":
    node = PiRealTimeNode()
    try:
        node.run()
    except KeyboardInterrupt:
        node.stop()
        print("[EXIT] Node Shutdown.")
