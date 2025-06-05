#!/bin/bash

echo "[🔁] Activating virtual environment..."
source venv/Scripts/activate || { echo "❌ Failed to activate venv"; exit 1; }

echo "[🤖] Starting PepeProphet bot in background..."
python main.py &

echo "[📅] Starting retrainer scheduler in background..."
python retrain_schedule.py &

echo "[🖥️] Launching Streamlit web terminal..."
streamlit run web_terminal.py
