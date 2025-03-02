[app]

# Název aplikace (zobrazí se třeba na ploše Androidu)
title = Battery Charge Tracker

# Jméno balíčku (bez mezer, typicky malé písmo a podtržítka)
package.name = battery_charge_tracker

# Doménu můžeš nechat klidně defaultní, nebo dát vlastní
package.domain = org.ondradol

# Cesta k souborům aplikace - tečka znamená "tady v této složce"
source.dir = .

# Jaké přípony souborů Buildozer zahrne do balíčku
source.include_exts = py,kv,txt,png,jpg,md

# Verze aplikace
version = 0.1

# Seznam Python balíčků (knihoven), které potřebuješ pro běh appky
# Minimálně python3, kivy, kivymd, pyjnius, cython
requirements = python3,kivy,kivymd,pyjnius,cython

# Jestli se má appka zobrazovat jen na výšku, nebo i na šířku (portrait/landscape)
orientation = portrait

# Minimální API level Androidu (tady dáme 33 pro Android 13)
android.sdk_api = 33

# Verze Build Tools, abys nepoužíval preview (např. 36-rc5)
android.sdk_build_tools = 33.0.0

# Možné architektury: armeabi-v7a, arm64-v8a, x86... 
# Většinou stačí ty dvě arm varianty
android.arch = armeabi-v7a,arm64-v8a

# -----------------------------------------------------------------------------
# Další nastavení buildozeru
# -----------------------------------------------------------------------------
[buildozer]

# Detaily logování, 1 = nejpodrobnější, 2 = střední
log_level = 2

# Když spustíš build jako root, Buildozer si postěžuje.
# Můžeš nastavit 0 = potlačit varování, 1 = povolit varování
warn_on_root = 1
