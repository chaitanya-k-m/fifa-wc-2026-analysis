"""
FIFA WC 2026 — LIVE STATS CLEANING
Flatten multi-header scraped CSVs -> clean Power BI-ready tables.
"""

import pandas as pd
import os

DATA = r"C:\Users\chait\Desktop\FIFA_WC_2026\Data"
CLEAN = os.path.join(DATA, "Clean")
os.makedirs(CLEAN, exist_ok=True)


# 1. PLAYER SUMMARY
print("Cleaning player_summary...")
ps = pd.read_csv(f"{DATA}\\player_summary_raw.csv",
                 header=[0, 1], index_col=[0, 1, 2, 3, 4])
ps.columns = ["jersey", "pos", "age", "min", "Gls", "Ast", "PK", "PKatt", "Sh", "SoT",
              "CrdY", "CrdR", "Fls", "Fld", "Off", "Crs", "TklW", "Int", "OG", "PKwon", "PKcon", "game_id"]
ps = ps.reset_index()
ps.columns = ["league", "season", "game",
              "team", "player"] + list(ps.columns[5:])
ps.to_csv(f"{CLEAN}\\player_summary_clean.csv",
          index=False, encoding="utf-8-sig")
print(f"  -> {ps.shape}")

# 2. PLAYER KEEPERS
print("Cleaning player_keepers...")
pk = pd.read_csv(f"{DATA}\\player_keepers_raw.csv",
                 header=[0, 1], index_col=[0, 1, 2, 3, 4])
pk.columns = ["age", "min", "SoTA", "GA", "Saves", "Save%", "game_id"]
pk = pk.reset_index()
pk.columns = ["league", "season", "game",
              "team", "player"] + list(pk.columns[5:])
pk.to_csv(f"{CLEAN}\\player_keepers_clean.csv",
          index=False, encoding="utf-8-sig")
print(f"  -> {pk.shape}")

# 3. PLAYER SEASON STANDARD
print("Cleaning player_season_standard...")
pss = pd.read_csv(f"{DATA}\\player_season_standard_raw.csv",
                  header=[0, 1], index_col=[0, 1, 2, 3])
pss.columns = ["nation", "pos", "age", "club", "born",
               "MP", "Starts", "Min", "90s",
               "Gls", "Ast", "G+A", "G-PK", "PK", "PKatt", "CrdY", "CrdR",
               "Gls_per90", "Ast_per90", "G+A_per90", "G-PK_per90", "G+A-PK_per90"]
pss = pss.reset_index()
pss.columns = ["league", "season", "team", "player"] + list(pss.columns[4:])
pss.to_csv(f"{CLEAN}\\player_season_clean.csv",
           index=False, encoding="utf-8-sig")
print(f"  -> {pss.shape}")

# 4. TEAM SHOOTING  (WC group stage only)
print("Cleaning team_shooting...")
tsh = pd.read_csv(f"{DATA}\\team_shooting_raw.csv",
                  header=[0, 1], index_col=[0, 1, 2, 3])
tsh.columns = ["date", "round", "day", "venue", "result", "GF", "GA", "opponent",
               "Gls", "Sh", "SoT", "SoT%", "G/Sh", "G/SoT", "PK", "PKatt", "time", "match_report"]
tsh = tsh.reset_index()
tsh.columns = ["league", "season", "team", "game"] + list(tsh.columns[4:])
tsh = tsh[tsh["round"].astype(str).str.contains(
    "Group stage", case=False, na=False)]
tsh.to_csv(f"{CLEAN}\\team_shooting_clean.csv",
           index=False, encoding="utf-8-sig")
print(f"  -> {tsh.shape}")

# 5. TEAM MISC  (WC group stage only)
print("Cleaning team_misc...")
tm = pd.read_csv(f"{DATA}\\team_misc_raw.csv", header=[
                 0, 1], index_col=[0, 1, 2, 3])
tm.columns = ["date", "round", "day", "venue", "result", "GF", "GA", "opponent",
              "CrdY", "CrdR", "2CrdY", "Fls", "Fld", "Off", "Crs", "Int", "TklW",
              "PKwon", "PKcon", "OG", "time", "match_report"]
tm = tm.reset_index()
tm.columns = ["league", "season", "team", "game"] + list(tm.columns[4:])
tm = tm[tm["round"].astype(str).str.contains(
    "Group stage", case=False, na=False)]
tm.to_csv(f"{CLEAN}\\team_misc_clean.csv", index=False, encoding="utf-8-sig")
print(f"  -> {tm.shape}")

print("\n\nDONE — clean files in:", CLEAN)
