import os
import glob
import pandas as pd
from datetime import datetime

def get_latest_signal_log():
    log_files = glob.glob("logs/signals_2025-*.csv")
    if not log_files:
        raise FileNotFoundError("No log files found.")
    return max(log_files, key=os.path.getctime)

latest_log = get_latest_signal_log()
print(f"[Labeler] Using latest log: {latest_log}")
df = pd.read_csv(latest_log)

# Simple price movement labeling
df['future_price'] = df['price'].shift(-1)
df['result'] = df.apply(lambda row: "WIN" if row['future_price'] > row['price'] else "LOSE", axis=1)

df.to_csv(latest_log, index=False)
print("[Labeler] Labeling complete and saved.")
