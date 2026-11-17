"""
FIFA WC 2026 — LIVE STATS CLEANING
Flatten multi-header scraped CSVs -> clean Power BI-ready tables,
then enrich with country flag columns (step 6).
"""

import pandas as pd
import os
from add_flag_columns import run as add_flags

DATA = r"C:\Users\chait\Desktop\Claude\Football\FIFA_WC_2026\Data"
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

# 4. TEAM SHOOTING  (WC finals only: June 11 onward = group + knockouts)
print("Cleaning team_shooting...")
tsh = pd.read_csv(f"{DATA}\\team_shooting_raw.csv",
                  header=[0, 1], index_col=[0, 1, 2, 3])
tsh.columns = ["date", "round", "day", "venue", "result", "GF", "GA", "opponent",
               "Gls", "Sh", "SoT", "SoT%", "G/Sh", "G/SoT", "PK", "PKatt", "time", "match_report"]
tsh = tsh.reset_index()
tsh.columns = ["league", "season", "team", "game"] + list(tsh.columns[4:])
tsh = tsh[tsh["game"].astype(str).str[:10] >= "2026-06-11"]
tsh.to_csv(f"{CLEAN}\\team_shooting_clean.csv",
           index=False, encoding="utf-8-sig")
print(f"  -> {tsh.shape}")

# 5. TEAM MISC  (WC finals only: June 11 onward = group + knockouts)
print("Cleaning team_misc...")
tm = pd.read_csv(f"{DATA}\\team_misc_raw.csv", header=[
                 0, 1], index_col=[0, 1, 2, 3])
tm.columns = ["date", "round", "day", "venue", "result", "GF", "GA", "opponent",
              "CrdY", "CrdR", "2CrdY", "Fls", "Fld", "Off", "Crs", "Int", "TklW",
              "PKwon", "PKcon", "OG", "time", "match_report"]
tm = tm.reset_index()
tm.columns = ["league", "season", "team", "game"] + list(tm.columns[4:])
tm = tm[tm["game"].astype(str).str[:10] >= "2026-06-11"]
tm.to_csv(f"{CLEAN}\\team_misc_clean.csv", index=False, encoding="utf-8-sig")
print(f"  -> {tm.shape}")

# 6. FLAG ENRICHMENT — adds country_code + flag_url to all clean files,
#    rewriting them as plain utf-8 (no BOM) so Power BI reads headers correctly.
print("\nAdding flag columns...")
add_flags(clean_dir=CLEAN, verify=False)

print("\n\nDONE — clean + flagged files in:", CLEAN)
