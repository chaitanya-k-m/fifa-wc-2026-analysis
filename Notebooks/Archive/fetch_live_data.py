import requests
import pandas as pd
import os

# ─────────────────────────────────────────────
# CONFIG — token is read from .env (FOOTBALL_DATA_TOKEN), never hard-coded
# ─────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv()
API_TOKEN = os.getenv("FOOTBALL_DATA_TOKEN")
OUTPUT_PATH = r"C:\Users\chait\Desktop\Claude\Football\FIFA_WC_2026\Data\live_wc2026.csv"

# ─────────────────────────────────────────────
# FETCH WC 2026 MATCHES
# ─────────────────────────────────────────────
url = "https://api.football-data.org/v4/competitions/WC/matches"

headers = {
    "X-Auth-Token": API_TOKEN
}

response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    matches = data["matches"]

    rows = []
    for m in matches:
        rows.append({
            "match_date": m["utcDate"][:10],
            "stage": m["stage"],
            "group": m.get("group", ""),
            "home_team": m["homeTeam"]["name"],
            "away_team": m["awayTeam"]["name"],
            "home_score": m["score"]["fullTime"]["home"],
            "away_score": m["score"]["fullTime"]["away"],
            "status": m["status"]
        })

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {len(df)} matches to {OUTPUT_PATH}")
    print(df.head(10))

else:
    print(f"Error: {response.status_code}")
    print(response.json())
