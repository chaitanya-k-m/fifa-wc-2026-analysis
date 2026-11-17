import pandas as pd
DATA = r"C:\Users\chait\Desktop\Claude\Football\FIFA_WC_2026\Data"
tsh = pd.read_csv(f"{DATA}\\team_shooting_raw.csv",
                  header=[0, 1], index_col=[0, 1, 2, 3])
tsh.columns = ["date", "round", "day", "venue", "result", "GF", "GA", "opponent",
               "Gls", "Sh", "SoT", "SoT%", "G/Sh", "G/SoT", "PK", "PKatt", "time", "match_report"]
print(tsh["round"].value_counts())
