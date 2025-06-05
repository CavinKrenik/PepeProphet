import os
import joblib
import schedule
import time
from train_model import train_from_csv

# === Enhanced Financial Signal Prediction ===
def predict_action(score, price, volume, sentiment, model_path="model.pkl"):
    try:
        model = joblib.load(model_path)
        probability = model.predict_proba([[score, price, volume, sentiment]])[0][1]  # probability of WIN

        if probability >= 0.85:
            return "📈 Strong Buy"
        elif probability >= 0.65:
            return "👍 Buy"
        elif probability >= 0.36:
            return "🤝 Hold"
        elif probability >= 0.15:
            return "👎 Sell"
        else:
            return "📉 Strong Sell"
    except Exception as e:
        print(f"[Predictor] Error loading or using model: {e}")
        return "🤝 Hold"

# === Retrain Routine ===
def retrain():
    print("[Retrainer] Running labeler and trainer...")
    os.system("python label_results.py")
    train_from_csv()
    print("[Retrainer] Completed daily retraining.")

if __name__ == "__main__":
    print("[Retrainer] Scheduled daily retraining at 12:00 PM.")
    schedule.every().day.at("12:00").do(retrain)

    while True:
        schedule.run_pending()
        time.sleep(60)
