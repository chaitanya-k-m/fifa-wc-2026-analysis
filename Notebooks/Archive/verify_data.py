import pandas as pd

data_dir = r"C:\Users\chait\Desktop\Claude\Football\FIFA_WC_2026\Data"

# Read just the index columns (skip the multi-header mess, read raw)
shoot = pd.read_csv(f"{data_dir}\\team_shooting_raw.csv", skiprows=2)
misc = pd.read_csv(f"{data_dir}\\team_misc_raw.csv", skiprows=2)

# The 'team' column is the 4th column (index 3) based on the structure we saw
shoot_teams = set(shoot.iloc[:, 3].unique())
misc_teams = set(misc.iloc[:, 3].unique())

print("Teams in shooting:", len(shoot_teams))
print("Teams in misc:", len(misc_teams))
print("\nIn shooting but NOT in misc:", shoot_teams - misc_teams)
print("In misc but NOT in shooting:", misc_teams - shoot_teams)
