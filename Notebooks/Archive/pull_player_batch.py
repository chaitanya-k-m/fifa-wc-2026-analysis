import soccerdata as sd

fbref = sd.FBref(leagues="INT-World Cup", seasons="2026", headless=False)

schedule = fbref.read_schedule()
played = schedule[schedule["score"].notna()].copy()
match_ids = played["game_id"].dropna().tolist()

out_dir = r"C:\Users\chait\Desktop\FIFA_WC_2026\Data"

print(f"Pulling remaining valid stat types for {len(match_ids)} matches.\n")

print("\n===== player keepers =====")
gk = fbref.read_player_match_stats(stat_type="keepers", match_id=match_ids)
gk.to_csv(f"{out_dir}\\player_keepers_raw.csv", encoding="utf-8-sig")
print(f"SAVED player_keepers: {gk.shape}")

print("\n===== team shooting =====")
team_shoot = fbref.read_team_match_stats(stat_type="shooting")
team_shoot.to_csv(f"{out_dir}\\team_shooting_raw.csv", encoding="utf-8-sig")
print(f"SAVED team_shooting: {team_shoot.shape}")

print("\n===== team misc =====")
team_misc = fbref.read_team_match_stats(stat_type="misc")
team_misc.to_csv(f"{out_dir}\\team_misc_raw.csv", encoding="utf-8-sig")
print(f"SAVED team_misc: {team_misc.shape}")

print("\n\nALL DONE.")
