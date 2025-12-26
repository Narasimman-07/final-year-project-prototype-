# tamper_monitor.py
# -----------------------
# Watches a specific file while the program runs.
# If its hash changes, a tampering alert is printed.

import time
import hashlib

class TamperMonitor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.original_hash = self._calculate_hash()

    def _calculate_hash(self):
        """
        Returns current SHA-256 hash of the monitored file.
        """
        h = hashlib.sha256()
        with open(self.file_path, 'rb') as f:
            while chunk := f.read(4096):
                h.update(chunk)
        return h.hexdigest()

    def watch(self):
        """
        Periodically recalculates hash and compares with original.
        """
        while True:
            current_hash = self._calculate_hash()
            if current_hash != self.original_hash:
                print("⚠️  Runtime Tampering Detected!")
                break
            time.sleep(5)  # check every 5 seconds
