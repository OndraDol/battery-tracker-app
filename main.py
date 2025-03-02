import os
from datetime import datetime, timedelta

from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from jnius import autoclass, cast

# -----------------------------------------------------------------------------
# ANDROID / BATTERY API
# -----------------------------------------------------------------------------
BatteryManager = autoclass('android.os.BatteryManager')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
IntentFilter = autoclass('android.content.IntentFilter')
Context = autoclass('android.content.Context')
Build = autoclass('android.os.Build')
BuildVersion = autoclass('android.os.Build$VERSION')
sdk_int = BuildVersion.SDK_INT

NotificationManager = autoclass('android.app.NotificationManager')
if sdk_int >= 26:
    NotificationChannel = autoclass('android.app.NotificationChannel')
NotificationBuilder = autoclass('android.app.Notification$Builder')

# Pro pokusné zjištění kapacity (může, ale nemusí fungovat na starších zařízeních)
try:
    BATTERY_PROPERTY_CAPACITY = BatteryManager.BATTERY_PROPERTY_CAPACITY
except:
    BATTERY_PROPERTY_CAPACITY = None

LOG_FILE = "battery_log.csv"

def create_notification_channel():
    """Create a notification channel for Android 8.0+."""
    activity = PythonActivity.mActivity
    notificationManager = cast(
        'android.app.NotificationManager',
        activity.getSystemService(Context.NOTIFICATION_SERVICE)
    )
    channel_id = "battery_channel"
    channel_name = "Battery Service"
    if sdk_int >= 26:
        importance = NotificationManager.IMPORTANCE_LOW
        channel = NotificationChannel(channel_id, channel_name, importance)
        notificationManager.createNotificationChannel(channel)
    return channel_id, notificationManager

def update_notification_text(text, channel_id, notificationManager):
    """Update or create a persistent notification with the given text."""
    activity = PythonActivity.mActivity
    if sdk_int >= 26:
        builder = NotificationBuilder(activity, channel_id)
    else:
        builder = NotificationBuilder(activity)
    builder.setContentTitle("Battery")
    builder.setContentText(text)
    appInfo = activity.getApplicationInfo()
    icon_id = appInfo.icon
    builder.setSmallIcon(icon_id)
    builder.setOngoing(True)
    notification = builder.build()
    notificationManager.notify(1, notification)

# -----------------------------------------------------------------------------
# KV CODE
# -----------------------------------------------------------------------------
kv = r'''
#:import dp kivy.metrics.dp
#:import MDSeparator kivymd.uix.card.MDSeparator

<CustomToolbar@MDBoxLayout>:
    size_hint_y: None
    height: dp(56)
    md_bg_color: app.theme_cls.primary_color
    padding: dp(10)
    MDLabel:
        text: "Battery Charge Tracker"
        halign: "center"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        font_style: "H6"

<MainScreen>:
    orientation: "vertical"

    # Jednoduchá náhrada za toolbar
    CustomToolbar:

    ScrollView:
        MDBoxLayout:
            orientation: "vertical"
            padding: dp(20)   # Zvýšené odsazení
            spacing: dp(20)   # Větší mezery mezi kartami
            size_hint_y: None
            height: self.minimum_height

            # KARTA PRO DNEŠNÍ NABITÍ
            MDCard:
                orientation: "vertical"
                padding: dp(25)    # Více místa uvnitř karty
                spacing: dp(15)
                elevation: 8
                radius: [20,]
                md_bg_color: 0.12, 0.12, 0.12, 1
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    id: today_label
                    text: "Charged Today: 0%"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    font_style: "H5"

                MDProgressBar:
                    id: today_progress
                    value: 0
                    max: 100
                    color: 0, 1, 0, 1

            # KARTA PRO OSTATNÍ STATISTIKY
            MDCard:
                orientation: "vertical"
                padding: dp(25)
                spacing: dp(15)
                elevation: 8
                radius: [20,]
                md_bg_color: 0.12, 0.12, 0.12, 1
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    id: week_label
                    text: "Last 7 Days: 0%"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    font_style: "Subtitle1"

                MDSeparator:
                    height: dp(1)
                    color: 1, 1, 1, 0.2

                MDLabel:
                    id: month_label
                    text: "Last 30 Days: 0%"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    font_style: "Subtitle1"

                MDSeparator:
                    height: dp(1)
                    color: 1, 1, 1, 0.2

                MDLabel:
                    id: year_label
                    text: "Last Year: 0%"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    font_style: "Subtitle1"

                MDSeparator:
                    height: dp(1)
                    color: 1, 1, 1, 0.2

                MDLabel:
                    id: lifetime_label
                    text: "Lifetime: 0%"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    font_style: "Subtitle1"

            # KARTA PRO POKROČILÉ INFO O BATERII
            MDCard:
                orientation: "vertical"
                padding: dp(25)
                spacing: dp(15)
                elevation: 8
                radius: [20,]
                md_bg_color: 0.12, 0.12, 0.12, 1
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: "Advanced Battery Info"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    font_style: "H6"

                MDSeparator:
                    height: dp(1)
                    color: 1, 1, 1, 0.2

                MDLabel:
                    id: battery_health_label
                    text: "Health: Unknown"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1

                MDSeparator:
                    height: dp(1)
                    color: 1, 1, 1, 0.2

                MDLabel:
                    id: battery_temp_label
                    text: "Temperature: ???"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1

                MDSeparator:
                    height: dp(1)
                    color: 1, 1, 1, 0.2

                MDLabel:
                    id: battery_voltage_label
                    text: "Voltage: ???"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1

                MDSeparator:
                    height: dp(1)
                    color: 1, 1, 1, 0.2

                MDLabel:
                    id: battery_tech_label
                    text: "Technology: ???"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1

                MDSeparator:
                    height: dp(1)
                    color: 1, 1, 1, 0.2

                MDLabel:
                    id: battery_status_label
                    text: "Status: ???"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1

                MDSeparator:
                    height: dp(1)
                    color: 1, 1, 1, 0.2

                MDLabel:
                    id: battery_plug_label
                    text: "Plug Type: ???"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1

                MDSeparator:
                    height: dp(1)
                    color: 1, 1, 1, 0.2

                MDLabel:
                    id: battery_present_label
                    text: "Battery Present: ???"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1

                MDSeparator:
                    height: dp(1)
                    color: 1, 1, 1, 0.2

                MDLabel:
                    id: battery_capacity_label
                    text: "Capacity: ???"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1

            # TLAČÍTKO PRO RUČNÍ AKTUALIZACI
            MDFillRoundFlatButton:
                text: "Update Stats"
                pos_hint: {"center_x": 0.5}
                on_release: root.update_stats()
'''

# -----------------------------------------------------------------------------
# MAIN SCREEN
# -----------------------------------------------------------------------------
class MainScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Vytvoření notifikačního kanálu
        self.channel_id, self.notificationManager = create_notification_channel()
        # Log baterie každých 5 minut
        Clock.schedule_interval(self.log_battery, 300)
        # Aktualizace statistik (a notifikace) každou minutu
        Clock.schedule_interval(lambda dt: self.update_stats(), 60)
        # První update hned po startu
        Clock.schedule_once(lambda dt: self.update_stats(), 1)

    def get_battery_level(self):
        """Get current battery level as a percentage."""
        intent = PythonActivity.mActivity.registerReceiver(
            None, IntentFilter("android.intent.action.BATTERY_CHANGED")
        )
        level = intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
        scale = intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
        if level != -1 and scale != -1:
            return (level / float(scale)) * 100
        return None

    def log_battery(self, dt):
        """Log the current battery level into a CSV file."""
        level = self.get_battery_level()
        if level is None:
            return
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_file = not os.path.exists(LOG_FILE)
        try:
            with open(LOG_FILE, "a", newline="") as csvfile:
                import csv
                writer = csv.writer(csvfile)
                if new_file:
                    writer.writerow(["timestamp", "battery"])
                writer.writerow([now, level])
        except Exception as e:
            print("Error logging battery level:", e)

    def calculate_stat(self, start_time):
        """Calculate difference between min and max battery in a given time range."""
        if not os.path.exists(LOG_FILE):
            return None
        battery_values = []
        try:
            with open(LOG_FILE, "r") as csvfile:
                import csv
                reader = csv.DictReader(csvfile)
                for row in reader:
                    ts = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
                    if ts >= start_time:
                        battery_values.append(float(row["battery"]))
        except Exception as e:
            print("Error reading log:", e)
            return None
        if battery_values:
            return max(battery_values) - min(battery_values)
        else:
            return None

    def get_advanced_info(self):
        """Získá podrobné informace z battery intentu."""
        intent = PythonActivity.mActivity.registerReceiver(
            None, IntentFilter("android.intent.action.BATTERY_CHANGED")
        )

        # Health map
        health_map = {
            1: "Unknown",
            2: "Good",
            3: "Overheat",
            4: "Dead",
            5: "Over Voltage",
            6: "Unspecified Failure",
            7: "Cold",
        }

        # Status map
        status_map = {
            1: "Unknown",
            2: "Charging",
            3: "Discharging",
            4: "Not Charging",
            5: "Full",
        }

        # Plug map
        plug_map = {
            1: "AC",
            2: "USB",
            4: "Wireless",
        }

        health_int = intent.getIntExtra(BatteryManager.EXTRA_HEALTH, 1)
        temperature_int = intent.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, 0)  # v desetinách °C
        voltage_int = intent.getIntExtra(BatteryManager.EXTRA_VOLTAGE, 0)         # v mV
        tech_str = intent.getStringExtra(BatteryManager.EXTRA_TECHNOLOGY)
        status_int = intent.getIntExtra(BatteryManager.EXTRA_STATUS, 1)
        plugged_int = intent.getIntExtra(BatteryManager.EXTRA_PLUGGED, 0)
        present_bool = intent.getBooleanExtra(BatteryManager.EXTRA_PRESENT, True)

        # Zkusíme získat kapacitu (může vrátit -1 nebo 0, pokud není podporováno)
        capacity_str = "???"
        try:
            battery_service = cast('android.os.BatteryManager',
                                   PythonActivity.mActivity.getSystemService(Context.BATTERY_SERVICE))
            if BATTERY_PROPERTY_CAPACITY:
                cap_val = battery_service.getIntProperty(BATTERY_PROPERTY_CAPACITY)
                if cap_val > 0:
                    capacity_str = f"{cap_val}%"
                else:
                    capacity_str = "N/A"
        except Exception as e:
            print("Capacity not available:", e)

        info = {}
        info["health"] = health_map.get(health_int, "Unknown")
        info["temperature"] = f"{temperature_int / 10.0:.1f} °C" if temperature_int > 0 else "???"
        info["voltage"] = f"{voltage_int / 1000.0:.2f} V" if voltage_int > 0 else "???"
        info["technology"] = tech_str if tech_str else "???"
        info["status"] = status_map.get(status_int, "Unknown")
        info["plug"] = plug_map.get(plugged_int, "None")
        info["present"] = "Yes" if present_bool else "No"
        info["capacity"] = capacity_str

        return info

    def update_stats(self):
        """Update labels and notification with calculated stats + advanced info."""
        now = datetime.now()
        periods = {
            "today": now.replace(hour=0, minute=0, second=0, microsecond=0),
            "7days": now - timedelta(days=7),
            "30days": now - timedelta(days=30),
            "year": now - timedelta(days=365),
            "lifetime": datetime.min
        }

        stat_today = self.calculate_stat(periods["today"])
        stat_7days = self.calculate_stat(periods["7days"])
        stat_30days = self.calculate_stat(periods["30days"])
        stat_year = self.calculate_stat(periods["year"])
        stat_lifetime = self.calculate_stat(periods["lifetime"])

        # Charged Today
        if stat_today is not None:
            self.ids.today_label.text = f"Charged Today: {stat_today:.1f}%"
            update_notification_text(
                f"Charged Today: {stat_today:.1f}%",
                self.channel_id,
                self.notificationManager
            )
            progress_value = min(stat_today, 100)
            self.ids.today_progress.value = progress_value
            self.ids.today_progress.color = (0, 1, 0, 1) if stat_today < 100 else (1, 0, 0, 1)
        else:
            self.ids.today_label.text = "Charged Today: 0%"
            update_notification_text("Charged Today: 0%", self.channel_id, self.notificationManager)
            self.ids.today_progress.value = 0

        # Ostatní statistiky
        self.ids.week_label.text = f"Last 7 Days: {stat_7days:.1f}%" if stat_7days is not None else "Last 7 Days: 0%"
        self.ids.month_label.text = f"Last 30 Days: {stat_30days:.1f}%" if stat_30days is not None else "Last 30 Days: 0%"
        self.ids.year_label.text = f"Last Year: {stat_year:.1f}%" if stat_year is not None else "Last Year: 0%"
        self.ids.lifetime_label.text = f"Lifetime: {stat_lifetime:.1f}%" if stat_lifetime is not None else "Lifetime: 0%"

        # Advanced info
        info = self.get_advanced_info()
        self.ids.battery_health_label.text = f"Health: {info['health']}"
        self.ids.battery_temp_label.text = f"Temperature: {info['temperature']}"
        self.ids.battery_voltage_label.text = f"Voltage: {info['voltage']}"
        self.ids.battery_tech_label.text = f"Technology: {info['technology']}"
        self.ids.battery_status_label.text = f"Status: {info['status']}"
        self.ids.battery_plug_label.text = f"Plug Type: {info['plug']}"
        self.ids.battery_present_label.text = f"Battery Present: {info['present']}"
        self.ids.battery_capacity_label.text = f"Capacity: {info['capacity']}"

# -----------------------------------------------------------------------------
# APP
# -----------------------------------------------------------------------------
class BatteryApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Builder.load_string(kv)
        return MainScreen()

if __name__ == '__main__':
    BatteryApp().run()