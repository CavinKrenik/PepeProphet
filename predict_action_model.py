import joblib
import numpy as np

def predict_action(score, price, volume, sentiment, model_path="model.pkl"):
    try:
        model = joblib.load(model_path)
        X = np.array([[score, price, volume, sentiment]])
        prediction = model.predict(X)[0]
        confidence = round(100 * model.predict_proba(X).max(), 2)

        action_label = "BUY 🚀" if prediction == 1 else "SELL 🛑"
        return action_label, confidence
    except Exception as e:
        print(f"[Predictor] Error loading or using model: {e}")
        return "HOLD ⏸️", 0
