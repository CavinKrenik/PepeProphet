# PepeProphet 🤖📈
**An AI-powered meme coin prediction bot** that uses market data, social sentiment, and technical signals to predict BUY/SELL/HOLD actions for top crypto assets and meme coins.

---

## ✅ Features

- 🔁 Collects market + social data every hour (CoinGecko & DexScreener)
- 💬 Sentiment analysis via Reddit
- 📊 Scores each token and predicts BUY/SELL/HOLD
- 🧠 Trains and auto-retrains daily using past results
- 📦 Clean modular codebase (data, analysis, alerts, model)
- 🔔 Sends alerts to Telegram + Discord (if configured)

---

## 🧪 Requirements

Make sure you're in your virtual environment:

```bash
python -m venv venv
source venv/bin/activate    # macOS/Linux
.env\Scriptsctivate     # Windows PowerShell
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🏁 How to Run Everything

Use the **process manager** to start data collection and model retraining in parallel:

```bash
python start_all.py
```

You will see:
```
[Manager] Starting PepeProphet and retraining scheduler...
[Manager] All processes started. Press CTRL+C to stop.
```

---

## 📁 File Structure

- `main.py` – Runs the bot hourly, collects market data, sends alerts
- `retrain_schedule.py` – Auto-retrains model daily at 12:00 PM
- `predict_action_model.py` – Loads model and returns prediction
- `train_model.py` – Trains the model manually from logs
- `label_results.py` – Compares past predictions vs current prices to assign WIN/LOSE
- `start_all.py` – Launches `main.py` and `retrain_schedule.py` simultaneously
- `logs/` – CSV logs of every prediction
- `model.pkl` – Trained machine learning model

---

## 🔁 Maintaining the Bot

Daily:
```bash
python label_results.py      # Label past predictions
python train_model.py        # Retrain model if needed
```

---

## 📬 Optional Alerts Setup

Add your tokens to `.env` file:

```env
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
DISCORD_WEBHOOK=your_discord_webhook_url
```

---

## 💡 Tip: Customize

- Want to check data every 15 mins? Edit `time.sleep(3600)` in `main.py` to `time.sleep(900)`
- Want to retrain at 9AM? Edit `retrain_schedule.py`:
```python
schedule.every().day.at("09:00").do(retrain)
```

---

## 📊 Logs and Performance

CSV logs are saved in `logs/signals_YYYY-MM-DD.csv` and include:

- Timestamp
- Coin
- Price
- Volume
- Sentiment score
- Prediction (BUY/SELL/HOLD)
- Future price (after N minutes/hours)
- Result (WIN/LOSE)

You can use this data to retrain, analyze, or improve scoring.

---

## 🛠️ Built With

- Python 3.9+
- scikit-learn
- requests, pandas, schedule
- CoinGecko API, DexScreener API
- Reddit (via Pushshift or BeautifulSoup)# PepeProphet
