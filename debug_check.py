import os
import sys

def check_project():
    print("--- Microplastic Project Diagnostics ---")
    
    # 1. Check root files
    root_files = ['app.py', 'requirements.txt', 'yolov8n.pt']
    for f in root_files:
        exists = os.path.exists(f)
        print(f"Root file '{f}': {'[OK]' if exists else '[MISSING]'}")

    # 2. Check src directory
    src_dir = os.path.join('src', 'core')
    if os.path.exists(src_dir):
        print(f"src/core directory: [OK]")
        for f in ['model_utils.py', 'hardware.py']:
            exists = os.path.exists(os.path.join(src_dir, f))
            print(f"  - {f}: {'[OK]' if exists else '[MISSING]'}")
    else:
        print("src/core directory: [MISSING]")

    # 3. Check micro-system
    ms_dir = 'microplastic-detection-system'
    if os.path.exists(ms_dir):
        print(f"{ms_dir} directory: [OK]")
        backend_app = os.path.join(ms_dir, 'backend', 'app.py')
        frontend_index = os.path.join(ms_dir, 'frontend', 'index.html')
        print(f"  - Backend app.py: {'[OK]' if os.path.exists(backend_app) else '[MISSING]'}")
        print(f"  - Frontend index.html: {'[OK]' if os.path.exists(frontend_index) else '[MISSING]'}")
    else:
        print(f"{ms_dir} directory: [MISSING]")

    # 4. Check dependencies
    try:
        import flask
        import flask_cors
        import cv2
        import ultralytics
        import streamlit
        print("Required Python packages: [OK]")
    except ImportError as e:
        print(f"Required Python packages: [ERR] - Missing {e.name}")

    print("\nSuggestions:")
    print("1. To run the main dashboard, use: streamlit run app.py")
    print("2. To run the micro-system backend, use: cd microplastic-detection-system/backend && python app.py")
    print("3. Ensure no other application is using your webcam.")

if __name__ == "__main__":
    check_project()
