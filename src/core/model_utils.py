import cv2
import numpy as np
from ultralytics import YOLO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MicroplasticDetector:
    def __init__(self, model_path='yolov8n.pt'):
        """
        Initialize the detector with a YOLOv8 model.
        Defaults to yolov8n (Nano) for speed on edge devices.
        """
        try:
            self.model = YOLO(model_path)
            logger.info(f"Model loaded successfully from {model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model = None

    def predict(self, image_np, conf_threshold=0.25):
        """
        Perform detection on an image.
        Returns annotated image, total count, and classification counts.
        """
        if self.model is None:
            return image_np, 0, {}

        results = self.model(image_np, conf=conf_threshold)
        
        # Parse results
        annotated_frame = results[0].plot() # Bounding boxes and labels
        
        # Count particles
        counts = {"fiber": 0, "fragment": 0, "bead": 0}
        total_count = 0
        
        # Map class indices to names (Assuming ordering: 0:fiber, 1:fragment, 2:bead)
        # Note: If using COCO pretrained model, these mapping won't match. 
        # This is built for the custom trained weight.
        class_names = results[0].names
        
        for box in results[0].boxes:
            class_id = int(box.cls[0])
            name = class_names[class_id].lower()
            if name in counts:
                counts[name] += 1
            else:
                counts[name] = counts.get(name, 0) + 1
            total_count += 1
            
        return annotated_frame, total_count, counts

    def estimate_size(self, box, scale_microns_per_pixel):
        """
        Estimate particle size based on bounding box and optical scale.
        """
        w_px = box[2] - box[0]
        h_px = box[3] - box[1]
        size_microns = max(w_px, h_px) * scale_microns_per_pixel
        return size_microns
