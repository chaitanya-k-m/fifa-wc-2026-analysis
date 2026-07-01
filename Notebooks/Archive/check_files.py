import pandas as pd
import os
d = r"C:\Users\chait\Desktop\FIFA_WC_2026\Data"
for f in ["live_wc2026.csv", "player_summary_raw.csv", "player_keepers_raw.csv", "team_shooting_raw.csv", "team_misc_raw.csv"]:
    p = os.path.join(d, f)
    exists = os.path.exists(p)
    size = os.path.getsize(p) if exists else 0
    print(f"{f:30} exists={exists}  size={size:,} bytes")
