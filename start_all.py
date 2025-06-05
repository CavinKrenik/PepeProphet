from multiprocessing import Process
import os

def start_main():
    os.system("python main.py")

def start_schedule():
    os.system("python retrain_schedule.py")

if __name__ == "__main__":
    print("[Manager] Starting PepeProphet and retraining scheduler...")
    Process(target=start_main).start()
    Process(target=start_schedule).start()
    print("[Manager] All processes started. Press CTRL+C to stop.")
