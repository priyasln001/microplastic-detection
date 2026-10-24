import cv2
from ultralytics import YOLO
import sys

def run_inference(image_path, model_path='yolov8n.pt'):
    # Load model
    model = YOLO(model_path)
    
    # Run detection
    results = model(image_path)
    
    # Show results
    for result in results:
        result.show() # Display image with boxes
        
        # Print stats
        print(f"Total detected: {len(result.boxes)}")
        for box in result.boxes:
            print(f"Type: {result.names[int(box.cls[0])]}, Conf: {box.conf[0]:.2f}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_inference(sys.argv[1])
    else:
        print("Usage: python detect.py <image_path>")
