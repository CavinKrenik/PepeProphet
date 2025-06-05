#!/bin/bash
cd "$(dirname "$0")"

echo "[💻] Activating virtual environment..."
source venv/bin/activate

echo "[🔁] Starting PepeProphet bot..."
python main.py &

echo "[📅] Starting retrainer scheduler..."
python retrain_schedule.py &

echo "[🖥️] Starting PepeProphet terminal..."
streamlit run web_terminal.py
