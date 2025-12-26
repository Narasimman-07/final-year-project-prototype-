# environment.py
# -----------------------
# Collects information about the current device and OS.
# Used for environment fingerprinting.

import uuid
import platform

def get_fingerprint():
    """
    Returns a dictionary containing a unique device ID and OS information.
    """
    device_id = str(uuid.getnode())  # uses the MAC address as a unique ID
    os_info = f"{platform.system()} {platform.release()}"
    return {
        "device_id": device_id,
        "os_info": os_info
    }
