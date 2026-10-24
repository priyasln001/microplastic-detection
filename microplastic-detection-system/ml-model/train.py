from ultralytics import YOLO
import os

def train_segmentation():
    """
    Template script for training YOLOv8 on microplastics dataset.
    Requires data.yaml to be present in the dataset folder.
    """
    # Load pretrained model
    model = YOLO('yolov8n.pt') 

    # Train (Using dummy data.yaml path for demonstration)
    # The actual train data would be located in ../dataset/
    model.train(
        data='data.yaml', 
        epochs=10, 
        imgsz=640, 
        device='cpu' # Use GPU if available
    )
    
    print("Training Complete. Model saved in runs/detect/train/weights/best.pt")

if __name__ == "__main__":
    print("Microplastic AI Training System")
    # train_segmentation() # Uncomment to run actual training
