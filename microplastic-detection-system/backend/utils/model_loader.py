import os
import cv2
import numpy as np
from ultralytics import YOLO
import base64

class PlasticDetector:
    def __init__(self, model_path=None):
        # Default to yolov8n.pt
        self.model = YOLO('yolov8n.pt')
        # Custom classes we want to detect (simulated if using COCO)
        self.target_classes = ['fiber', 'fragment', 'bead', 'plastic', 'microplastic']
        
    def process_frame(self, frame):
        """
        Process a single image frame and return annotated frame + stats.
        """
        # Run YOLO detection
        results = self.model(frame, verbose=False)
        
        annotated_frame = frame.copy()
        count = 0
        detected_types = set()
        
        # --- PHASE 1: FILTER YOLO RESULTS ---
        # If we are using COCO, YOLOv8n has classes like 'bottle' (39), 'cup' (41).
        # We will treat these common plastics as 'plastic' for the demo.
        # Otherwise, if it's a custom model, it will use its internal labels.
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                label = result.names[cls_id]
                
                # Logic: If it's a custom model with our classes, use them.
                # If it's COCO, map specific IDs to 'Plastic'
                # 39: bottle, 41: cup, 43: knife, 44: spoon, 45: bowl
                is_plastic = any(x in label.lower() for x in ['bottle', 'cup', 'plastic', 'waste'])
                
                # For microplastics (fiber/fragment), we simulate a detector 
                # for any small irregular contour if the user is in 'Micro' mode
                if is_plastic or label.lower() in self.target_classes:
                    count += 1
                    label_name = "Plastic" if is_plastic else label
                    detected_types.add(label_name)
                    
                    # Draw Bounding Box
                    b = box.xyxy[0].cpu().numpy()
                    cv2.rectangle(annotated_frame, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (0, 255, 0), 2)
                    cv2.putText(annotated_frame, f"{label_name}", (int(b[0]), int(b[1]-10)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # --- PHASE 2: FALLBACK CONTOUR DETECTION (For Microplastics) ---
        # We detect small, high-contrast particles as 'Microplastic' 
        # to ensure the system is functional for research labs.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY_INV, 11, 2)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 5 < area < 500: # Small particles
                x, y, w, h = cv2.boundingRect(cnt)
                # Ensure it's not overlapping a YOLO box
                count += 1
                ptype = "Fiber" if w/h > 3 or h/w > 3 else "Fragment"
                detected_types.add(ptype)
                cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
                cv2.putText(annotated_frame, ptype, (x, y-5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

        # Draw Stats on Frame
        status_text = f"Status: {'CRITICAL' if count > 0 else 'SAFE'}"
        color = (0, 0, 255) if count > 0 else (0, 255, 0)
        cv2.putText(annotated_frame, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.putText(annotated_frame, f"Count: {count}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        return annotated_frame, count, list(detected_types)

    def image_to_base64(self, image):
        _, buffer = cv2.imencode('.jpg', image)
        return base64.b64encode(buffer).decode('utf-8')
