import pandas as pd

# Load the data
results = pd.read_csv(
    r"C:\Users\chait\Desktop\Claude\Football\FIFA_WC_2026\Data\Raw\results.csv")
elo = pd.read_csv(
    r"C:\Users\chait\Desktop\Claude\Football\FIFA_WC_2026\Data\Raw\elo_ratings_wc2026.csv")

# ── RESULTS ──────────────────────────────────
print("=== SHAPE ===")
print(results.shape)

print("\n=== FIRST 5 ROWS ===")
print(results.head())

print("\n=== COLUMN TYPES ===")
print(results.info())

print("\n=== NULLS ===")
print(results.isnull().sum())

print("\n=== BASIC STATS ===")
print(results.describe())

print("\n=== UNIQUE TOURNAMENTS ===")
print(results["tournament"].value_counts().head(20))

print("\n=== DUPLICATES ===")
print(results.duplicated().sum())

# ── ELO ──────────────────────────────────────
print("\n\n=== ELO SHAPE ===")
print(elo.shape)

print("\n=== ELO FIRST 5 ROWS ===")
print(elo.head())

print("\n=== ELO NULLS ===")
print(elo.isnull().sum())
