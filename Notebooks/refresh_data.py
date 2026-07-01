"""
FIFA WC 2026 — RAW DATA REFRESH PIPELINE
Pulls live match data (API) + scrapes player/team stats (FBref via soccerdata).
Run this whenever new matches are played to refresh the raw data layer.
"""

import os
import requests
import pandas as pd
import soccerdata as sd
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
load_dotenv()  # reads .env from project root
API_TOKEN = os.getenv("FOOTBALL_DATA_TOKEN")

DATA_DIR = r"C:\Users\chait\Desktop\FIFA_WC_2026\Data"

if not API_TOKEN:
    raise SystemExit(
        "ERROR: FOOTBALL_DATA_TOKEN not found. Check your .env file in the project root.")

# ─────────────────────────────────────────────
# STEP 1 — LIVE MATCH DATA (football-data.org API)
# ─────────────────────────────────────────────
print("\n===== STEP 1: Live match data (API) =====")
url = "https://api.football-data.org/v4/competitions/WC/matches"
resp = requests.get(url, headers={"X-Auth-Token": API_TOKEN})

if resp.status_code == 200:
    matches = resp.json()["matches"]
    rows = [{
        "match_date": m["utcDate"][:10],
        "stage": m["stage"],
        "group": m.get("group", ""),
        "home_team": m["homeTeam"]["name"],
        "away_team": m["awayTeam"]["name"],
        "home_score": m["score"]["fullTime"]["home"],
        "away_score": m["score"]["fullTime"]["away"],
        "status": m["status"],
    } for m in matches]
    pd.DataFrame(rows).to_csv(
        f"{DATA_DIR}\\live_wc2026.csv", index=False, encoding="utf-8-sig")
    print(f"  Saved {len(rows)} matches -> live_wc2026.csv")
else:
    print(
        f"  API ERROR {resp.status_code} — skipping live data, keeping existing file.")

# ─────────────────────────────────────────────
# STEP 2 — SETUP FBREF SCRAPER
# ─────────────────────────────────────────────
print("\n===== STEP 2: FBref scraper setup =====")
fbref = sd.FBref(leagues="INT-World Cup", seasons="2026", headless=False)
schedule = fbref.read_schedule()
played = schedule[schedule["score"].notna()].copy()
match_ids = played["game_id"].dropna().tolist()
print(f"  {len(match_ids)} played matches found.")

# ─────────────────────────────────────────────
# STEP 3 — PLAYER STATS (per match)
# ─────────────────────────────────────────────
print("\n===== STEP 3: Player stats =====")
player_summary = fbref.read_player_match_stats(
    stat_type="summary", match_id=match_ids)
player_summary.to_csv(
    f"{DATA_DIR}\\player_summary_raw.csv", encoding="utf-8-sig")
print(f"  Saved player_summary: {player_summary.shape}")

player_keepers = fbref.read_player_match_stats(
    stat_type="keepers", match_id=match_ids)
player_keepers.to_csv(
    f"{DATA_DIR}\\player_keepers_raw.csv", encoding="utf-8-sig")
print(f"  Saved player_keepers: {player_keepers.shape}")

# ─────────────────────────────────────────────
# STEP 4 — PLAYER SEASON TOTALS (per-90 metrics)
# ─────────────────────────────────────────────
print("\n===== STEP 4: Player season totals =====")
season_std = fbref.read_player_season_stats(stat_type="standard")
season_std.to_csv(
    f"{DATA_DIR}\\player_season_standard_raw.csv", encoding="utf-8-sig")
print(f"  Saved player_season_standard: {season_std.shape}")

# ─────────────────────────────────────────────
# STEP 5 — TEAM STATS (per team match)
# ─────────────────────────────────────────────
print("\n===== STEP 5: Team stats =====")
team_shooting = fbref.read_team_match_stats(stat_type="shooting")
team_shooting.to_csv(
    f"{DATA_DIR}\\team_shooting_raw.csv", encoding="utf-8-sig")
print(f"  Saved team_shooting: {team_shooting.shape}")

team_misc = fbref.read_team_match_stats(stat_type="misc")
team_misc.to_csv(f"{DATA_DIR}\\team_misc_raw.csv", encoding="utf-8-sig")
print(f"  Saved team_misc: {team_misc.shape}")

print("\n\n===== REFRESH COMPLETE =====")
print("All raw data saved to:", DATA_DIR)
