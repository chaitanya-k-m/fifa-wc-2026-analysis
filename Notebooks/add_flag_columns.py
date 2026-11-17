"""
FIFA WC 2026 — FLAG URL ENRICHMENT
Adds `country_code` (ISO 3166-1 alpha-2, lowercase) and `flag_url`
(flagcdn.com) columns to the cleaned CSVs, keyed off each file's
country-name source column.

Reusable step: import `add_flags_to_file` / `run` from refresh_data.py
or clean_live_stats.py so every future data refresh re-applies it.
"""

import os
import pandas as pd
import pycountry
import requests

DATA = r"C:\Users\chait\Desktop\Claude\Football\FIFA_WC_2026\Data"
CLEAN = os.path.join(DATA, "Clean")

FLAG_URL_TEMPLATE = "https://flagcdn.com/w80/{code}.png"

# Files to enrich, mapped to the column holding the country name.
# For international football, "team" == country.
FLAG_TARGETS = {
    "player_season_clean.csv": "nation",
    "player_keepers_clean.csv": "team",
    "player_summary_clean.csv": "team",
    "team_shooting_clean.csv": "team",
    "team_misc_clean.csv": "team",
}

# Manual overrides for strings pycountry can't (or shouldn't) resolve
# alone — either non-ISO entities (home nations) or spelling variants
# that differ across FBref scrape/source files.
MANUAL_OVERRIDES = {
    "Korea Republic": "kr",
    "Côte d'Ivoire": "ci",
    "Curaçao": "cw",
    "Türkiye": "tr",
    "Congo DR": "cd",
    "Bosnia & Herz.": "ba",
    "Bosnia and Herzegovina": "ba",
    "Bosnia–Herz": "ba",
    "Bosnia-Herz": "ba",
    "United States": "us",
    "IR Iran": "ir",
    # Home nations aren't ISO countries; flagcdn serves them as
    # UK subdivision flags.
    "England": "gb-eng",
    "Scotland": "gb-sct",
    "Wales": "gb-wls",
    "Northern Ireland": "gb-nir",
}


def resolve_country_code(name: str) -> str | None:
    """Look up an ISO 3166-1 alpha-2 (or flagcdn subdivision) code for a country name."""
    if name in MANUAL_OVERRIDES:
        return MANUAL_OVERRIDES[name]
    try:
        return pycountry.countries.lookup(name).alpha_2.lower()
    except LookupError:
        return None


def build_country_code_map(names) -> dict:
    """Build {name: code} for every distinct country name, validating full coverage.

    Prints every unmapped name (not just the first) so overrides can be
    added in one pass, then raises — callers must not silently proceed
    with missing flags.
    """
    mapping = {name: resolve_country_code(name) for name in names}
    unmapped = sorted(n for n, code in mapping.items() if code is None)
    if unmapped:
        print(
            f"\n[add_flag_columns] {len(unmapped)} unmapped country name(s):")
        for n in unmapped:
            print(f"    {n!r}")
        raise ValueError(
            "Unmapped country names found — add entries to MANUAL_OVERRIDES "
            "in add_flag_columns.py and re-run: " +
            ", ".join(repr(n) for n in unmapped)
        )
    return mapping


def add_flag_columns(df: pd.DataFrame, country_col: str, code_map: dict) -> pd.DataFrame:
    """Return a copy of df with `country_code` and `flag_url` columns added."""
    df = df.copy()
    df["country_code"] = df[country_col].map(code_map)
    df["flag_url"] = df["country_code"].map(
        lambda c: FLAG_URL_TEMPLATE.format(code=c) if pd.notna(c) else None
    )
    return df


def verify_sample_urls(urls, sample_size: int = 5) -> None:
    """HEAD-check a sample of flag URLs and print their status codes."""
    urls = sorted(set(urls))
    sample = urls[:sample_size]
    print(
        f"\n[add_flag_columns] Verifying {len(sample)} sample flag URL(s)...")
    for url in sample:
        try:
            resp = requests.head(url, timeout=10, allow_redirects=True)
            print(f"    {resp.status_code}  {url}")
        except requests.RequestException as e:
            print(f"    ERR   {url}  ({e})")


def run(clean_dir: str = CLEAN, verify: bool = True) -> None:
    """Apply flag enrichment to all FLAG_TARGETS files in clean_dir, in place."""
    print("\n===== Adding flag URL columns =====")

    # 1. Union all distinct country-name strings across every source column.
    all_names = set()
    frames = {}
    for filename, col in FLAG_TARGETS.items():
        path = os.path.join(clean_dir, filename)
        # utf-8-sig strips a BOM if present (e.g. from before this fix) and
        # reads plain utf-8 files identically otherwise.
        df = pd.read_csv(path, encoding="utf-8-sig")
        frames[filename] = df
        all_names.update(df[col].dropna().unique().tolist())
    print(f"  {len(all_names)} distinct country name(s) found across {len(FLAG_TARGETS)} file(s).")

    # 2. Build + validate the {name: code} map (raises if anything is unmapped).
    code_map = build_country_code_map(all_names)

    # 3. Add columns and write each file back.
    for filename, col in FLAG_TARGETS.items():
        df = add_flag_columns(frames[filename], col, code_map)
        path = os.path.join(clean_dir, filename)
        df.to_csv(path, index=False, encoding="utf-8")
        print(f"  -> {filename}: {df.shape}")

    # 4. Optional sample HEAD-check.
    if verify:
        sample_urls = [
            FLAG_URL_TEMPLATE.format(code=code) for code in code_map.values()
        ]
        verify_sample_urls(sample_urls)

    print("\nDONE — flag columns added in:", clean_dir)


if __name__ == "__main__":
    run()
