import mysql.connector
import pandas as pd
import os


raw_results = r"C:\Users\chait\Desktop\Claude\Football\FIFA_WC_2026\Data\Raw\results.csv"
raw_elo = r"C:\Users\chait\Desktop\Claude\Football\FIFA_WC_2026\Data\Raw\elo_ratings_wc2026.csv"

results = pd.read_csv(raw_results)
elo = pd.read_csv(raw_elo)

results["date"] = pd.to_datetime(results["date"])
print(results["date"].dtype)
results = results.dropna(subset=["home_score", "away_score"])
print(results.shape)


results["home_score"] = results["home_score"].astype(int)
results["away_score"] = results["away_score"].astype(int)
print(results[["home_score", "away_score"]].dtypes)


results["year"] = results["date"].dt.year
results = results[results["year"] >= 1930]
print(results.shape)


def get_result(row):
    if row["home_score"] > row["away_score"]:
        return "home_win"
    elif row["home_score"] < row["away_score"]:
        return "away_win"
    else:
        return "draw"


results["result"] = results.apply(get_result, axis=1)
print(results["result"].value_counts())


clean_path = r"C:\Users\chait\Desktop\Claude\Football\FIFA_WC_2026\Data\Clean\results_clean.csv"
results.to_csv(clean_path, index=False)
print("Saved.")


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    port=3306
)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS wc2026;")
cursor.execute("USE wc2026;")

cursor.execute("DROP TABLE IF EXISTS results;")
cursor.execute("""
    CREATE TABLE results (
        id          INT AUTO_INCREMENT PRIMARY KEY,
        date        DATE,
        year        INT,
        home_team   VARCHAR(100),
        away_team   VARCHAR(100),
        home_score  INT,
        away_score  INT,
        tournament  VARCHAR(200),
        city        VARCHAR(100),
        country     VARCHAR(100),
        neutral     BOOLEAN,
        result      VARCHAR(20)
    );
""")

cols = ["date", "year", "home_team", "away_team", "home_score",
        "away_score", "tournament", "city", "country", "neutral", "result"]

insert_sql = """
    INSERT INTO results (date,year,home_team,away_team,home_score,
                         away_score,tournament,city,country,neutral,result)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

data = results[cols].where(pd.notnull(results[cols]), None)
cursor.executemany(insert_sql, data.values.tolist())
conn.commit()

print(f"Inserted {cursor.rowcount} rows into wc2026.results")
cursor.close()
conn.close()
