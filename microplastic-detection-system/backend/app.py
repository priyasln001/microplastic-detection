from flask import Flask, render_template, Response, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import threading
import time
import os
from utils.model_loader import PlasticDetector

# Use absolute paths for stability
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='/')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Global variables for Camera Threading
camera = None
output_frame = None
lock = threading.Lock()
is_running = False

try:
    detector = PlasticDetector()
    print("[SYSTEM] ML Model loaded successfully.")
except Exception as e:
    print(f"[ERROR] Model loading failed: {e}")
    detector = None

def stream_camera():
    global camera, output_frame, is_running
    try:
        # Use CAP_DSHOW for faster startup on Windows
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not camera.isOpened():
            # Fallback to default
            camera = cv2.VideoCapture(0)
            
        if not camera.isOpened():
            print("[ERROR] Could not open webcam.")
            is_running = False
            return

        while is_running:
            success, frame = camera.read()
            if not success:
                break
            
            if detector:
                try:
                    # Run detection on current frame
                    processed_frame, count, types = detector.process_frame(frame)
                    with lock:
                        output_frame = processed_frame.copy()
                except Exception as e:
                    print(f"[ERROR] Detection failed: {e}")
                    with lock:
                        output_frame = frame.copy()
            else:
                with lock:
                    output_frame = frame.copy()
            
            time.sleep(0.01) # Reduce CPU usage
                
    except Exception as e:
        print(f"[ERROR] Camera thread crashed: {e}")
    finally:
        is_running = False
        if camera:
            camera.release()
            camera = None

def generate_frames():
    global output_frame, lock, is_running
    while True:
        if not is_running and output_frame is None:
            break
            
        with lock:
            if output_frame is None:
                time.sleep(0.1)
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", output_frame)
            if not flag:
                continue
        
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
        time.sleep(0.04)

@app.route('/video-feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start-camera', methods=['POST'])
def start_camera():
    global is_running, camera
    if not is_running:
        is_running = True
        t = threading.Thread(target=stream_camera)
        t.daemon = True
        t.start()
        
        # Give it a second to initialize
        time.sleep(1.5)
        if not is_running:
            return jsonify({"status": "error", "message": "Camera failed to start"}), 500
            
        return jsonify({"status": "Camera started"})
    return jsonify({"status": "Already running"})

@app.route('/stop-camera', methods=['POST'])
def stop_camera():
    global is_running, output_frame
    is_running = False
    with lock:
        output_frame = None
    return jsonify({"status": "Camera stopped"})

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image"}), 400
    file = request.files['image']
    import numpy as np
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return jsonify({"error": "Invalid image data"}), 400
    
    if detector:
        res, count, types = detector.process_frame(img)
        return jsonify({
            "microplastic_detected": count > 0,
            "count": count,
            "types": types,
            "image": detector.image_to_base64(res)
        })
    else:
        return jsonify({"error": "Model not loaded"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

