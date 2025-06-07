import joblib
import pandas as pd

# Load model once
model = joblib.load("model.pkl")

def predict_action(score, price, volume, sentiment):
    features = pd.DataFrame([{
        "score": score,
        "price": price,
        "volume": volume,
        "sentiment": sentiment
    }])

    confidence = round(model.predict_proba(features)[0][1] * 100, 2)
    prediction = model.predict(features)[0]

    if prediction == 1:
        action = "BUY 🚀" if confidence > 60 else "HOLD ⏸️"
    else:
        action = "SELL 🛑" if confidence > 60 else "HOLD ⏸️"

    return action, confidence
