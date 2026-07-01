import soccerdata as sd

fbref = sd.FBref(
    leagues="INT-World Cup",
    seasons="2026",
    headless=False
)

# Pull team match stats — possession, shots, etc.
team_stats = fbref.read_team_match_stats(stat_type="schedule")
print("SHAPE:", team_stats.shape)
print(team_stats.columns.tolist())
print(team_stats.head())
