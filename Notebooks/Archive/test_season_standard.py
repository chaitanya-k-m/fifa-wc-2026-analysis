import soccerdata as sd

fbref = sd.FBref(leagues="INT-World Cup", seasons="2026", headless=False)

print("Pulling season 'standard' player stats...")
df = fbref.read_player_season_stats(stat_type="standard")

print("\nSHAPE:", df.shape)
print("\nALL COLUMNS:")
for col in df.columns.tolist():
    print("  ", col)

print("\nFIRST 3 ROWS:")
print(df.head(3).to_string())

# Save it so we have it regardless
out = r"C:\Users\chait\Desktop\FIFA_WC_2026\Data\player_season_standard_raw.csv"
df.to_csv(out, encoding="utf-8-sig")
print("\nSaved to:", out)
