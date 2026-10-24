from ultralytics import YOLO
import os

def train_model():
    """Trains the YOLOv8 model on the microplastics dataset."""
    
    # Load a pretrained YOLOv8 model (e.g., yolov8n - nano, yolov8s - small)
    model = YOLO('yolov8n.pt') 

    # Define path to the data.yaml created by prepare_dataset.py
    data_yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "microplastics_dataset", "data.yaml")

    print(f"Starting training using config: {data_yaml_path}")
    print("This may take a while depending on your hardware...")

    # Train the model
    # Note: Adjust epochs and imgsz based on your dataset and hardware capabilities.
    # For a real project, epochs > 50 is typical.
    results = model.train(
        data=data_yaml_path,
        epochs=10,        # Number of epochs
        imgsz=640,        # Image size
        device='cpu',     # Use '0' for GPU, 'cpu' for CPU
        project='runs/detect',
        name='microplastics_run1'
    )

    print("Training complete!")
    print(f"Best model saved to: {results.save_dir}/weights/best.pt")

if __name__ == "__main__":
    # Ensure data.yaml exists before training
    data_yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "microplastics_dataset", "data.yaml")
    if not os.path.exists(data_yaml_path):
        print(f"Error: {data_yaml_path} not found.")
        print("Please run prepare_dataset.py first and populate it with labeled data.")
    else:
        train_model()
