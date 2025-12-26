import hashlib
import os
import platform
import uuid

def calculate_file_hash(filepath):
    """Calculate SHA256 hash of a given file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_environment_fingerprint():
    """Collect system fingerprint (CPU, MAC, OS)."""
    mac = uuid.getnode()
    os_info = platform.system() + " " + platform.release()
    cpu = platform.processor() or "UnknownCPU"
    return f"{mac}-{os_info}-{cpu}"
