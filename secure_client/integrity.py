# integrity.py
# -----------------------
# Calculates SHA-256 hash of a file.
# This hash will be compared with the server-stored hash
# to detect tampering.

import hashlib

def generate_file_hash(filepath):
    """
    Reads the file and returns its SHA-256 hash string.
    """
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        # Read file in chunks for efficiency
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()
