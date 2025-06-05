import streamlit as st
import pandas as pd
import joblib
from predict_action_model import predict_action

st.set_page_config(page_title="PepeProphet Terminal", layout="wide")
st.title("📈 PepeProphet AI Terminal")

st.markdown("Monitor predictions, trigger retrains, and explore live market signals.")

# === Load latest CSV ===
import glob
import os

latest_file = max(glob.glob("logs/signals_*.csv"), key=os.path.getctime)

st.subheader("🧾 Latest Signals")
df = pd.read_csv(latest_file)
st.dataframe(df.tail(20), use_container_width=True)

# === Prediction Tool ===
st.subheader("🔍 Manual Prediction")

score = st.slider("Score", 0.0, 1.0, 0.5)
price = st.number_input("Price", value=0.01)
volume = st.number_input("Volume", value=1000.0)
sentiment = st.slider("Sentiment", -1.0, 1.0, 0.0)

if st.button("Predict Action"):
    action = predict_action(score, price, volume, sentiment)
    st.success(f"🔮 Predicted Action: **{action}**")

# === Model Trigger ===
st.subheader("⚙️ Model Controls")

if st.button("Run Retrain"):
    os.system("python label_results.py && python train_model.py")
    st.success("✅ Model retrained successfully!")

