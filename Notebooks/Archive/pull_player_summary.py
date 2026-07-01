import soccerdata as sd
import pandas as pd

fbref = sd.FBref(leagues="INT-World Cup", seasons="2026", headless=False)

# Get game_ids for played matches (from cached schedule — instant)
schedule = fbref.read_schedule()
played = schedule[schedule["score"].notna()].copy()
match_ids = played["game_id"].dropna().tolist()

print(f"Pulling player summary stats for {len(match_ids)} matches...")
print("This will take ~15-25 min. The browser will open. Let it run.")

# Pull player match stats — summary type
player_summary = fbref.read_player_match_stats(
    stat_type="summary",
    match_id=match_ids
)

print("DONE — shape:", player_summary.shape)
print("COLUMNS:", player_summary.columns.tolist())

# Save raw output
out = r"C:\Users\chait\Desktop\FIFA_WC_2026\Data\player_summary_raw.csv"
player_summary.to_csv(out, encoding="utf-8-sig")
print("Saved to:", out)
print(player_summary.head())
