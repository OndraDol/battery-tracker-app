[app]

# Název aplikace
title = Battery Charge Tracker

# Jméno balíčku (bez mezer)
package.name = battery_charge_tracker

# Doménu klidně nech, jak chceš
package.domain = org.ondradol

# Cesta k souborům aplikace
source.dir = .

# Jaké přípony souborů Buildozer zahrne
source.include_exts = py,kv,txt,png,jpg,md

# Verze
version = 0.1

# Seznam Python balíčků
requirements = python3,kivy,kivymd,pyjnius,cython


[buildozer]
# Vynucení konkrétní větve p4a
p4a.branch = develop

# Explicitní cesta k p4a
p4a.source_dir = ./python-for-android


# Orientace (portrait/landscape)
orientation = portrait

# Minimální API level (Android 13 = 33)
android.sdk_api = 33

# Použij stabilní build-tools (ne 36-rcX!)
android.sdk_build_tools = 33.0.0

# Architektury
android.archs = armeabi-v7a,arm64-v8a

# -----------------------------------------------------------------------------
# (Nepovinné) Další nastavení buildozeru
# -----------------------------------------------------------------------------
[buildozer]
log_level = 2
warn_on_root = 1
