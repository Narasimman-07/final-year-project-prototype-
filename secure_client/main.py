# main.py
# -----------------------
# Entry point for the Secure Client.
# 1. Generates    file hash and fingerprint.
# 2. Sends them to the Django attestation server.
# 3. Starts a background monitor to 

import requests
from integrity import generate_file_hash
from environment import get_fingerprint
from tamper_monitor import TamperMonitor
import threading

# URL of your Django API endpoint
SERVER_URL = "http://127.0.0.1:8000/api/verify/"

def send_to_server(app_name, file_path):
    """
    Sends file hash and fingerprint data to the attestation server.
    """
    fingerprint = get_fingerprint()
    hash_value = generate_file_hash(file_path)

    data = {
        "app_name": app_name,
        "hash": hash_value,
        "device_id": fingerprint["device_id"],
        "os_info": fingerprint["os_info"]
    }

    try:
        response = requests.post(SERVER_URL, json=data)
        print("Server Response:", response.json())
    except Exception as e:
        print("❌ Could not reach server:", e)

if __name__ == "__main__":
    APP_NAME = "SecureFramework"
    FILE_PATH = "main.py"  # this file will be checked for tampering

    # Step 1 — Send initial hash to the server
    send_to_server(APP_NAME, FILE_PATH)

    # Step 2 — Start runtime tamper detection in background
    monitor = TamperMonitor(FILE_PATH)
    thread = threading.Thread(target=monitor.watch)
    thread.start()
