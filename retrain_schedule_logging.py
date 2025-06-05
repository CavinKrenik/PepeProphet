import schedule
import time
from train_model import train_from_csv
from logger_setup import setup_logger

# Initialize logger from shared setup
logger = setup_logger("logs/pepeprophet_retrain.log")

def retrain():
    logger.info("🚀 Starting daily model retraining...")
    try:
        train_from_csv()
        logger.info("✅ Retraining complete.")
    except Exception as e:
        logger.error(f"❌ Retraining failed: {e}")

# Schedule retraining at noon every day
schedule.every().day.at("12:00").do(retrain)
logger.info("📅 Scheduled daily retraining at 12:00 PM.")

# Loop to check for scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(60)
