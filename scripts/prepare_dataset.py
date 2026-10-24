import os
import shutil

def setup_directory_structure(base_path):
    """Creates the necessary folder structure for the dataset."""
    dirs = [
        "train/images", "train/labels",
        "val/images", "val/labels",
        "test/images", "test/labels"
    ]
    for d in dirs:
        os.makedirs(os.path.join(base_path, d), exist_ok=True)
    print(f"Directory structure created at {base_path}")

def generate_yaml(base_path):
    """Generates the data.yaml file required for YOLOv8 training."""
    yaml_content = f"""
train: {os.path.join(base_path, 'train/images')}
val: {os.path.join(base_path, 'val/images')}
test: {os.path.join(base_path, 'test/images')}

nc: 3
names: ['fiber', 'fragment', 'bead']
"""
    with open(os.path.join(base_path, "data.yaml"), "w") as f:
        f.write(yaml_content)
    print("data.yaml generated.")

if __name__ == "__main__":
    dataset_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "microplastics_dataset")
    setup_directory_structure(dataset_dir)
    generate_yaml(dataset_dir)
    print("Dataset setup complete. Please place your images and YOLO format txt labels in the respective folders.")
