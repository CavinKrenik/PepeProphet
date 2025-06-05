import streamlit as st
import os
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="PepeProphet Terminal", layout="wide")

# 🔁 Auto-refresh every 60 seconds
st_autorefresh = st.empty()
st_autorefresh.markdown(
    f"<meta http-equiv='refresh' content='60'>",
    unsafe_allow_html=True
)

st.title("🧠 PepeProphet AI Terminal")

# 📈 Bot Status
st.subheader("📈 Bot Status")
log_file = "logs/pepeprophet_main.log"
last_log_line = ""
if os.path.exists(log_file):
    with open(log_file, "r") as f:
        lines = f.readlines()
        if lines:
            last_log_line = lines[-1]

st.text(f"🕒 Last Log Entry:\n{last_log_line.strip() if last_log_line else 'No entries yet.'}")

# 📊 Live CSV Viewer
st.subheader("📊 Today's Signal Data")
log_csv = f"logs/signals_{datetime.now().strftime('%Y-%m-%d')}.csv"
if os.path.exists(log_csv):
    df = pd.read_csv(log_csv)
    st.dataframe(df.tail(20))
    if 'price' in df.columns and 'volume' in df.columns:
        st.line_chart(df[['price', 'volume']])
else:
    st.warning("No signal log for today yet.")

# 📜 Live Logs Viewer
st.subheader("📜 Live Logs")
if os.path.exists(log_file):
    with open(log_file, "r") as f:
        logs = f.read()
    st.text_area("Log Output", logs, height=300)
else:
    st.warning("Log file not found.")
