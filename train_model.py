import pandas as pd
import os
import joblib
from datetime import datetime  # <-- Needed for backup timestamp
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_from_csv(csv_path="logs/pepeprophet_signals.csv", model_path="model.pkl"):
    if not os.path.exists(csv_path):
        print(f"[Trainer] CSV log file not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)

    if 'result' not in df.columns:
        print("[Trainer] 'result' column missing. Add WIN/LOSE tracking first.")
        return

    df = df[df['action'].str.contains("BUY|SELL", na=False)]
    df = df[df['result'].isin(["WIN", "LOSE"])]

    if df.empty:
        print("[Trainer] No valid training data found.")
        return

    X = df[['score', 'price', 'volume', 'sentiment']]
    y = df['result'].apply(lambda x: 1 if x == "WIN" else 0)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"[Trainer] Accuracy: {accuracy:.2f}")

    joblib.dump(model, model_path)
    print(f"[Trainer] Model saved to {model_path}")

    # ✅ Versioned backup
    os.makedirs("model_backups", exist_ok=True)
    backup_name = f"model_backups/model_{datetime.now().strftime('%Y%m%d_%H%M')}.pkl"
    joblib.dump(model, backup_name)
    print(f"[Trainer] Backup saved to {backup_name}")

if __name__ == "__main__":
    train_from_csv()
