import os
import pandas as pd
from datetime import datetime
import streamlit as st
from PIL import Image

st.set_page_config(page_title="PepeProphet Terminal", layout="wide")

# Load image and display title
image = Image.open("prof.png")
st.image(image, width=50)
st.markdown("## PepeProphet AI Terminal")

# Uptime
if "start_time" not in st.session_state:
    st.session_state["start_time"] = datetime.now()
    st.session_state["cycles"] = 0
st.session_state["cycles"] += 1

st.caption(f"🕒 Uptime: {datetime.now() - st.session_state['start_time']}, Cycles: {st.session_state['cycles']}")

# === Sidebar Filters ===
st.sidebar.header("🔍 Filter Signals")
today_log = f"logs/signals_{datetime.now().strftime('%Y-%m-%d')}.csv"
df = pd.read_csv(today_log, encoding="utf-8", on_bad_lines='skip') if os.path.exists(today_log) else pd.DataFrame()

coin_filter = st.sidebar.selectbox("Coin", ["All"] + sorted(df["coin"].unique()) if not df.empty else ["All"])
action_filter = st.sidebar.selectbox("Action", ["All", "BUY 🚀", "SELL 🛑", "HOLD ⏸️"])
confidence_range = st.sidebar.slider("Confidence % Range", 0, 100, (0, 100))

if not df.empty:
    if "confidence" not in df.columns:
        df["confidence"] = 0
    df = df[df["confidence"].between(confidence_range[0], confidence_range[1])]
    if coin_filter != "All":
        df = df[df["coin"] == coin_filter]
    if action_filter != "All":
        df = df[df["action"] == action_filter]

# === Signal Table ===
st.subheader("📊 Signal Log")
if not df.empty:
    df_sorted = df.sort_values("timestamp", ascending=False)
    st.dataframe(df_sorted, use_container_width=True)
else:
    st.warning("No data available for today.")

# === Confidence Meter ===
if not df.empty:
    st.subheader("📟 Confidence Gauge")
    for idx, row in df_sorted.iterrows():
        confidence = row["confidence"]
        color = "🟩 High" if confidence > 75 else "🟨 Medium" if confidence > 50 else "🟧 Low" if confidence > 25 else "🟥 Very Low"
        st.text(f"{row['timestamp']} | {row['coin']} | {row['action']} | Confidence: {confidence:.2f}% {color}")

# === Accuracy Tracking ===
acc_log = "logs/accuracy_log.csv"
if os.path.exists(acc_log):
    acc_df = pd.read_csv(acc_log)
    st.subheader("🎯 Accuracy Over Time")
    st.line_chart(acc_df.set_index("timestamp")["accuracy"])

# === Sentiment Score ===
sentiment_log = "logs/sentiment_score.txt"
if os.path.exists(sentiment_log):
    with open(sentiment_log) as f:
        sentiment = f.read().strip()
    st.subheader("🧠 Live Reddit Sentiment Score")
    st.metric(label="Current Sentiment", value=sentiment)

# === CSV Export ===
if not df.empty:
    csv_export = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", data=csv_export, file_name="pepeprophet_signals.csv", mime="text/csv")

# === Live Logs ===
st.subheader("📜 Live Logs")
log_file = "logs/pepeprophet_main.log"
if os.path.exists(log_file):
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            logs = f.read()
        st.text_area("Log Output", logs, height=300)
    except UnicodeDecodeError:
        st.warning("⚠️ Could not decode log file (non-UTF-8 characters).")
else:
    st.warning("⚠️ Log file not found.")

# === Retrain Button ===
st.subheader("🧠 Manual Retrain")
if st.button("🔁 Trigger Model Retrain"):
    os.system("python retrain_schedule.py")
    st.success("Retraining triggered!")

# === Top Trending Coin Placeholder ===
st.subheader("📊 Top Trending Coins (Coming Soon)")
st.info("We'll visualize most active coins based on volume/sentiment soon.")

# === TradingView Widget Instruction (for integration with React frontend) ===
st.subheader("💹 External Chart Integration")
st.markdown("To embed a TradingView widget, use the provided `TradingViewWidget.jsx` React component in your frontend.")