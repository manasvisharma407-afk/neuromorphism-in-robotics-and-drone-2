from datetime import datetime


class Logger:
    def __init__(self):
        pass

    def info(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[INFO] [{timestamp}] {message}")

    def alert(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[ALERT] [{timestamp}] {message}")