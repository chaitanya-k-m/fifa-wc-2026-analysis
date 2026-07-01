import soccerdata as sd

fbref = sd.FBref(leagues="INT-World Cup", seasons="2026", headless=False)

# CHECK 1: What player-level stat types does the library actually allow?
print("===== PLAYER stat types =====")
try:
    fbref.read_player_match_stats(stat_type="INVALID_TEST")
except Exception as e:
    print(e)

# CHECK 2: What player SEASON stat types exist? (different function — may have passing)
print("\n===== PLAYER SEASON stat types =====")
try:
    fbref.read_player_season_stats(stat_type="INVALID_TEST")
except Exception as e:
    print(e)
