import pandas as pd

DATA = r"C:\Users\chait\Desktop\FIFA_WC_2026\Data"

files = [
    "player_summary_raw.csv",
    "player_keepers_raw.csv",
    "player_season_standard_raw.csv",
    "team_shooting_raw.csv",
    "team_misc_raw.csv",
]

for f in files:
    print(f"\n{'='*60}\n{f}\n{'='*60}")
    # Read first 5 rows raw, no header parsing, to SEE the structure
    raw = pd.read_csv(f"{DATA}\\{f}", header=None, nrows=5)
    print(raw.to_string())
