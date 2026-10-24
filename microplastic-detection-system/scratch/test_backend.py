import requests

def test_backend():
    url = "http://localhost:5000"
    try:
        # Test start-camera
        print("Testing /start-camera...")
        resp = requests.post(f"{url}/start-camera")
        print(f"Response: {resp.status_code} - {resp.json()}")
        
        # Test stop-camera
        print("Testing /stop-camera...")
        resp = requests.post(f"{url}/stop-camera")
        print(f"Response: {resp.status_code} - {resp.json()}")
        
        return True
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        return False

if __name__ == "__main__":
    test_backend()
