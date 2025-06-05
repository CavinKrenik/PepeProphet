import os
import joblib
import schedule
import time

def retrain():
    os.system("python label_results.py")
    os.system("python train_model.py")

def predict_action(score, price, volume, sentiment, model_path="model.pkl"):
    try:
        model = joblib.load(model_path)
        prediction = model.predict([[score, price, volume, sentiment]])[0]
        return "BUY 🚀" if prediction == 1 else "SELL 🛑"
    except Exception as e:
        print(f"[Predictor] Error loading or using model: {e}")
        return "HOLD ⏸️"

if __name__ == "__main__":
    print("[Retrainer] Scheduled weekly retraining every Sunday at 12:00.")
    schedule.every().sunday.at("12:00").do(retrain)

    while True:
        schedule.run_pending()
        time.sleep(60)
