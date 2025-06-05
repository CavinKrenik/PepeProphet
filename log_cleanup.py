import os
import time
from datetime import datetime

LOG_DIR = "logs"
DAYS_TO_KEEP = 10

def delete_old_logs():
    now = time.time()
    cutoff = now - (DAYS_TO_KEEP * 86400)

    for filename in os.listdir(LOG_DIR):
        if filename.startswith("signals_") and filename.endswith(".csv"):
            filepath = os.path.join(LOG_DIR, filename)
            file_mtime = os.path.getmtime(filepath)

            if file_mtime < cutoff:
                os.remove(filepath)
                print(f"[Cleanup] Deleted old log file: {filename}")

if __name__ == "__main__":
    delete_old_logs()
