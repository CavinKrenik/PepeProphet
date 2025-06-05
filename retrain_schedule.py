import schedule
import time
import os

def retrain():
    print("[Retrainer] Starting daily retraining...")
    os.system("python label_results.py")
    os.system("python train_model.py")

schedule.every().day.at("12:00").do(retrain)

print("[Retrainer] Scheduled daily retraining at 12:00 PM.")
while True:
    schedule.run_pending()
    time.sleep(60)
