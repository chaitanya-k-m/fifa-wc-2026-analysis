import soccerdata as sd
import pandas as pd

fbref = sd.FBref(leagues="INT-World Cup", seasons="2026", headless=False)

# Schedule is already cached — this is instant
schedule = fbref.read_schedule()

# Keep only matches that have actually been played (have a score)
played = schedule[schedule["score"].notna()].copy()

print("Total matches in schedule:", len(schedule))
print("Matches played so far:", len(played))
print()
print("Played matches with game_ids:")
print(played[["home_team", "away_team", "score", "game_id"]].to_string())
