import pandas as pd
import os
from datetime import datetime, timedelta

def label_log_file(filepath):
    df = pd.read_csv(filepath)

    if "future_price" not in df.columns:
        df["future_price"] = ""
    if "result" not in df.columns:
        df["result"] = ""

    # Convert timestamp column to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    for i, row in df.iterrows():
        if pd.notna(row["result"]) and row["result"] != "":
            continue  # already labeled

        action = str(row["action"]).upper()
        if "BUY" not in action and "SELL" not in action:
            continue

        timestamp = row["timestamp"]
        price = row["price"]
        future_time = timestamp + timedelta(minutes=10)

        # Find future row for same coin
        future_rows = df[
            (df["coin"] == row["coin"]) &
            (df["timestamp"] > future_time)
        ]

        if future_rows.empty:
            continue

        future_price = future_rows.iloc[0]["price"]

        try:
            future_price = float(future_price)
            price = float(price)
        except:
            continue

        # Determine result
        if "BUY" in action:
            result = "WIN" if future_price > price else "LOSE"
        elif "SELL" in action:
            result = "WIN" if future_price < price else "LOSE"
        else:
            result = ""

        df.at[i, "future_price"] = future_price
        df.at[i, "result"] = result

    df.to_csv(filepath, index=False)
    print(f"[Labeler] Updated {filepath}")

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    path = f"logs/signals_{today}.csv"
    if os.path.exists(path):
        label_log_file(path)
    else:
        print(f"[Labeler] Log file not found: {path}")
