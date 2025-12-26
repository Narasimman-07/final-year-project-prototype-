import time
import requests
from utils import calculate_file_hash, get_environment_fingerprint

SERVER_URL = "http://127.0.0.1:8000/api/verify/"  # Your Django endpoint
APP_NAME = "SecureTestApp"
DEVICE_ID = "DEVICE_001"
MONITORED_FILE = "client_monitor.py"  

def verify_integrity():
    file_hash = calculate_file_hash(MONITORED_FILE)
    fingerprint = get_environment_fingerprint()

    payload = {
        "app_name": APP_NAME,
        "hash": file_hash,
        "device_id": DEVICE_ID,
        "os_info": fingerprint
    }

    try:
        res = requests.post(SERVER_URL, json=payload)
        print(f"Server Response: {res.json()}")
    except Exception as e:
        print("Error contacting server:", e)

def start_monitor(interval=10):
    """Continuously verify integrity every X seconds."""
    print(f"🔒 Starting integrity monitor for {APP_NAME}...")
    while True:
        verify_integrity()
        time.sleep(interval)

if __name__ == "__main__":
    start_monitor(interval=15)
