#!/bin/bash

cd "$(dirname "$0")"

echo "[Setup] Checking virtual environment..."

# Create virtual environment if missing
if [ ! -d "venv" ]; then
  echo "[Setup] Creating virtual environment..."
  python -m venv venv || { echo "❌ Python not found"; exit 1; }
fi

# Activate the virtual environment
source venv/Scripts/activate 2>/dev/null || source venv/bin/activate

# Upgrade pip + install requirements
echo "[Setup] Installing/updating requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Check required files exist
REQUIRED=("start_all.py" "main.py" "retrain_schedule.py" "requirements.txt" ".env")
for file in "${REQUIRED[@]}"; do
  if [ ! -f "$file" ]; then
    echo "❌ Missing required file: $file"
    exit 1
  fi
done

# Run the full system
echo "[Start] Starting PepeProphet bot & retrainer..."
python start_all.py || echo "❌ Error running start_all.py"
