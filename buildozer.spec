[app]
title = SingleFileBatteryTracker
package.name = single_file_battery_tracker
package.domain = org.ondradol
source.dir = .
source.include_exts = py
version = 0.1
requirements = python3,kivy,kivymd,pyjnius,cython
orientation = portrait

# P4A často ignoruje, ale zkusíme
android.sdk_api = 33
android.sdk_build_tools = 33.0.0
android.archs = armeabi-v7a,arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
