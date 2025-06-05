import os
import pandas as pd
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="PepeProphet Terminal", layout="wide")
st.markdown(f"<meta http-equiv='refresh' content='60'>", unsafe_allow_html=True)

# Uptime Tracking
if "start_time" not in st.session_state:
    st.session_state["start_time"] = datetime.now()
    st.session_state["cycles"] = 0
st.session_state["cycles"] += 1

st.title("📈 PepeProphet AI Terminal")
st.caption(f"🕒 Uptime: {datetime.now() - st.session_state['start_time']}, Cycles: {st.session_state['cycles']}")

# Load Logs
today_log = f"logs/signals_{datetime.now().strftime('%Y-%m-%d')}.csv"
df = pd.read_csv(today_log) if os.path.exists(today_log) else pd.DataFrame()

# Sidebar Filters
st.sidebar.header("🔍 Filter Signals")
coin_filter = st.sidebar.selectbox("Coin", ["All"] + sorted(df["coin"].unique()) if not df.empty else ["All"])
action_filter = st.sidebar.selectbox("Action", ["All", "BUY 🚀", "SELL 🛑", "HOLD ⏸️"])
if coin_filter != "All":
    df = df[df["coin"] == coin_filter]
if action_filter != "All":
    df = df[df["action"] == action_filter]

# Signal Table
st.subheader("📊 Signal Log")
if not df.empty:
    st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)
else:
    st.warning("No data available for today.")

# CSV Download
if not df.empty:
    csv_export = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", data=csv_export, file_name="pepeprophet_signals.csv", mime="text/csv")

# Accuracy Chart
model_log = "logs/accuracy_log.csv"
if os.path.exists(model_log):
    acc_df = pd.read_csv(model_log)
    st.subheader("🎯 Accuracy Over Time")
    st.line_chart(acc_df.set_index("timestamp")["accuracy"])

# Sentiment Score
sentiment_log = "logs/sentiment_score.txt"
if os.path.exists(sentiment_log):
    with open(sentiment_log) as f:
        sentiment = f.read().strip()
        st.subheader("🧠 Live Reddit Sentiment Score")
        st.metric(label="Current Sentiment", value=sentiment)

# Logs Viewer
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

