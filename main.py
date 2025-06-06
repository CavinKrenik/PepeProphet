from dotenv import load_dotenv
load_dotenv()

import os
import csv
import time
from datetime import datetime
from pepeprophet.data.dexscreener import fetch_dex_pair
from pepeprophet.data.market_data import fetch_market_data
from pepeprophet.data.social_scraper import fetch_reddit_posts
from pepeprophet.analysis.sentiment import analyze_sentiment
from pepeprophet.analysis.scoring import score_trend
from pepeprophet.notifications.telegram import send_telegram_alert
from pepeprophet.notifications.discord import send_discord_alert
from predict_action_model import predict_action
from logger_setup import setup_logger

logger = setup_logger("logs/pepeprophet_main.log")

def log_to_csv(coin, price, volume, sentiment, score, action, confidence, future_price=None, result=None):
    date_str = datetime.now().strftime('%Y-%m-%d')
    filepath = f"logs/signals_{date_str}.csv"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    file_exists = os.path.isfile(filepath)

    with open(filepath, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow([
                "timestamp", "coin", "price", "volume", "sentiment", "score", "action", "confidence", "future_price", "result"
            ])
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            coin, price, volume, sentiment, round(score, 3), action, confidence,
            future_price, result
        ])

def run_bot():
    while True:
        logger.info("🚀 Starting new hybrid prediction cycle...")
        print("[PepeProphet] Starting new hybrid prediction cycle...\n")

        coin_ids = ["bitcoin", "ethereum", "solana", "ripple"]
        market_data = fetch_market_data(coin_ids)

        for coin, data in market_data.items():
            logger.info(f"[Market] {coin.upper()} - Price: ${data['price']}, Volume: {data['volume']}")
            posts = fetch_reddit_posts()
            sentiment_score = analyze_sentiment(posts)
            score = score_trend(data, sentiment_score)

            try:
                action, confidence = predict_action(score, data["price"], data["volume"], sentiment_score)
            except Exception as e:
                logger.warning(f"[Predictor] Error: {e} — using fallback logic")
                action, confidence = ("BUY 🚀", 0) if score > 0.6 else ("SELL 🛑", 0) if score < 0.3 else ("HOLD ⏸️", 0)

            msg = (
                f"📊 {coin.upper()} Report\n"
                f"Score: {score:.3f}\n"
                f"Price: ${data['price']:,}\n"
                f"Volume: {data['volume']:,}\n"
                f"Sentiment: {sentiment_score:.2f}\n"
                f"Action: {action} ({confidence}% confidence)"
            )

            logger.info(f"[Alert] {coin.upper()} Action: {action} ({confidence}%)")
            send_telegram_alert(msg)
            send_discord_alert(msg)
            log_to_csv(coin.upper(), data["price"], data["volume"], sentiment_score, score, action, confidence)

        dex_pairs = {
            "MIND (Mind of Pepe)": "0xa339d4c41ad791e27a10cd0f9a80deec815b79ee",
            "WEPE (Wall Street Pepe)": "0xa3c2076eb97d573cc8842f1db1ecdf7b6f77ba27",
            "MOODENG": "ED5nyyWEzpPPiWimP8vYm7sD7TD3LAt3Q3gRTWHzPJBY"
        }

        for name, address in dex_pairs.items():
            logger.info(f"[DexScreener] Fetching {name}...")
            try:
                data = fetch_dex_pair(address)
                sentiment_score = 0
                score = score_trend(data, sentiment_score)
                action, confidence = predict_action(score, data["price"], data["volume"], sentiment_score)

                msg = (
                    f"📊 {name}\n"
                    f"Price: ${data['price']:.6f}\n"
                    f"Volume: {data['volume']:,.0f}\n"
                    f"Score: {score:.3f}\n"
                    f"Sentiment: {sentiment_score:.2f}\n"
                    f"Action: {action} ({confidence}% confidence)\n"
                    f"🔗 [View on DexScreener]({data['url']})"
                )

                logger.info(f"[Alert] {name} Action: {action} ({confidence}%)")
                send_telegram_alert(msg)
                send_discord_alert(msg)
                log_to_csv(name, data["price"], data["volume"], sentiment_score, score, action, confidence)
            except Exception as e:
                logger.error(f"[DexScreener Error] {name}: {e}")

        logger.info("✅ Cycle complete. Sleeping for 1 hour...\n")
        time.sleep(3600)

if __name__ == "__main__":
    run_bot()
