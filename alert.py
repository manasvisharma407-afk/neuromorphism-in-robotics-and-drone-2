from config import ALERT_CONFIDENCE_THRESHOLD
from utils.logger import Logger


class AlertManager:
    def __init__(self):
        self.logger = Logger()

    def send_alert(self, prediction, confidence):
        labels = {
            0: "No Threat",
            1: "Wildlife Detected",
            2: "Poacher Detected"
        }

        label = labels[prediction]

        print("\n=== ALERT SYSTEM ===")
        print("Prediction:", label)
        print("Confidence:", f"{confidence:.2f}")

        if prediction == 2 and confidence >= ALERT_CONFIDENCE_THRESHOLD:
            payload = {
                "type": "threat_alert",
                "priority": "high"
            }

            self.logger.alert("POACHER DETECTED")

            print("Payload:")
            print(payload)

            return payload

        return None