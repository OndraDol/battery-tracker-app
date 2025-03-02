import time
import os
import csv
from datetime import datetime
from jnius import autoclass

# Získání tříd z Android API
BatteryManager = autoclass('android.os.BatteryManager')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
IntentFilter = autoclass('android.content.IntentFilter')

LOG_FILE = "battery_log.csv"

def main():
    while True:
        # Získání stavu baterie
        intent = PythonActivity.mActivity.registerReceiver(None, IntentFilter("android.intent.action.BATTERY_CHANGED"))
        level = intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
        scale = intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
        if level != -1 and scale != -1:
            battery_level = (level / float(scale)) * 100
        else:
            battery_level = None

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if battery_level is not None:
            new_file = not os.path.exists(LOG_FILE)
            try:
                with open(LOG_FILE, "a", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    if new_file:
                        writer.writerow(["timestamp", "battery"])
                    writer.writerow([now, battery_level])
            except Exception as e:
                print("Chyba při logování:", e)
        # Logování každých 5 minut
        time.sleep(300)