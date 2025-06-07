# train_model.py
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
import os

log_dir = "logs"
log_files = [f for f in os.listdir(log_dir) if f.startswith("signals_") and f.endswith(".csv")]

dfs = []
for file in log_files:
    df = pd.read_csv(os.path.join(log_dir, file), encoding="utf-8", on_bad_lines='skip')
    dfs.append(df)

data = pd.concat(dfs, ignore_index=True)
data = data[data["result"].isin(["WIN", "LOSE"])]
data["target"] = data["result"].map({"WIN": 1, "LOSE": 0})

X = data[["score", "price", "volume", "sentiment"]]
y = data["target"]

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

joblib.dump(model, "model.pkl")
print("✅ Model retrained and saved as model.pkl")
