import os
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.image import AsyncImage
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from jnius import autoclass

# Příklad: Chceme přečíst úroveň baterie (placeholder, může se lišit podle zařízení)
# Tady si jen ukážeme, že to jde, reálně to na GitHub Actions nemusí fungovat.
BatteryManager = autoclass('android.os.BatteryManager')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
IntentFilter = autoclass('android.content.IntentFilter')

# Nahraď vlastním odkazem na logo
CSc_logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Android_robot.svg/600px-Android_robot.svg.png"

# KivyMD layout v jednom stringu
KV = r'''
#:import dp kivy.metrics.dp

<MainScreen>:
    orientation: "vertical"
    spacing: dp(20)
    padding: dp(20)

    MDCard:
        orientation: "vertical"
        size_hint_y: None
        height: self.minimum_height
        padding: dp(20)
        radius: [15,]
        md_bg_color: 0.12, 0.12, 0.12, 1
        elevation: 8

        # LOGO
        AsyncImage:
            id: csc_logo
            source: app.logo_url
            size_hint: (1, None)
            height: dp(150)
            keep_ratio: True
            allow_stretch: True

        MDLabel:
            id: text_label
            text: "Single-File Battery Tracker"
            halign: "center"
            font_style: "H5"
            size_hint_y: None
            height: self.texture_size[1] + dp(10)

        MDSeparator:
            height: dp(1)

        MDLabel:
            id: battery_label
            text: "Battery Level: ???"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1] + dp(10)

    MDFillRoundFlatButton:
        text: "Close App"
        pos_hint: {"center_x": 0.5}
        on_release: app.stop()
'''

class MainScreen(MDBoxLayout):
    pass

class BatteryApp(MDApp):
    logo_url = CSc_logo_url  # Můžeme takto předat URL loga do AsyncImage

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Builder.load_string(KV)
        # Naplánujeme aktualizaci baterie
        Clock.schedule_interval(self.update_battery, 5)
        return MainScreen()

    def update_battery(self, dt):
        # Placeholder logika pro baterii
        # (Na reálném telefonu to může fungovat, v GitHub Actions se jen odzkouší, že kód běží.)
        try:
            activity = PythonActivity.mActivity
            filter_ = IntentFilter("android.intent.action.BATTERY_CHANGED")
            intent = activity.registerReceiver(None, filter_)
            level = intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
            scale = intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
            if level != -1 and scale != -1:
                battery_pct = int((level / float(scale)) * 100)
                self.root.ids.battery_label.text = f"Battery Level: {battery_pct}%"
            else:
                self.root.ids.battery_label.text = "Battery Level: ???"
        except Exception as e:
            self.root.ids.battery_label.text = f"Battery Level: ??? (Error: {e})"

if __name__ == "__main__":
    BatteryApp().run()
