# FIFA World Cup 2026 — Performance Intelligence

An end-to-end analytics project built while the 2026 World Cup was being played. A Python pipeline pulls match, player and shot data from a sports-data API into raw JSON, flattens it into a star-schema set of clean CSVs, and feeds a multi-page Power BI report. Before that came historical work: 1872–2026 international results loaded into MySQL and analysed in SQL.

**Stack:** Python (pandas, requests), REST API integration, MySQL, Power BI (Power Query, DAX, data modelling), Tableau Public.

---

## What it answers

- How did the 2026 tournament play out: goals, xG, where and when goals were scored?
- Which teams scored more than their chances deserved (goals vs xG), and which scored less?
- For any one of the 104 matches: how did the xG race unfold, minute by minute, and who scored?
- Historically: which nations win most often, who is in form, what are the head-to-head records, how big is home advantage, and which World Cup had the most goals per game?

## Headline numbers (full tournament, 104 matches)

| Metric | Value |
|---|---|
| Matches | 104 (73 group, 16 round of 32, 8 round of 16, 4 quarter-finals, 2 semi-finals, final) |
| Goals credited to players | 294 (2.83 per match) |
| Team goals including own goals | 308 (the 14 extra are own goals; see below) |
| Shots | 2,633, of which 40 were shoot-out kicks and are excluded from every goal and xG figure |
| Goals in minutes 76–90 | 81, against 68 xG. Late goals beat expectation |
| Golden Boot (FIFA tiebreak) | Kylian Mbappé |
| Top keeper (clean sheets, then saves) | Unai Simón |

Every figure comes from the pipeline's final run and was checked against the clean CSVs.

---

## How the project evolved

The project went through three versions. Only the third is live, and the repo still holds the first two.

| Phase | Data | Output | Status |
|---|---|---|---|
| 1. Historical | International results 1872–2026 (49,378 rows) and Elo ratings | MySQL database, 6 SQL analyses, CSV exports, Tableau Public dashboard | Done |
| 2. Power BI v1 | FBref via the `soccerdata` library, plus football-data.org for live scores | 5 CSVs, first Overview dashboard | Abandoned: FBref shut down its advanced-stats feed in January 2026, and international matches never had passing or defending data there |
| 3. Power BI v2 | TheStatsAPI: player-level xG/xA, shot coordinates, passing, defending, duels | 8-table star schema, Overview and Matchups dashboards | **Current** |

## Data sources

- **TheStatsAPI** (phase 3): per-match `/stats`, `/player-stats`, `/shotmap`, `/lineups` and `/timeline`, plus team, squad, player and standings endpoints. It needs a paid key. The API has no heatmaps, event streams or tracking data (distance, sprints).
- **International football results, 1872–2026**, and **Elo ratings** (phase 1): `Data/Raw/`.
- **FBref** via `soccerdata`, and **football-data.org** (phase 2): `Data/*_raw.csv`, frozen.

---

## Pipeline (phase 3)

```
TheStatsAPI ──► snapshot.py ──► raw/ JSON ──► clean.py ──► clean/*.csv ──► Power BI
                (incremental,    per match,     (flatten,      8 tables
                 retry/backoff)   player, team   derive, flag)
                          refresh.py runs all steps in one command
```

- **`snapshot.py`** pulls every endpoint for each finished match, plus player and team reference data. Re-running it skips files that are already saved, so it resumes after an interruption and fetches only new matches. When rate-limited (HTTP 429) or on a server error it retries with backoff, and it logs anything it could not get instead of dropping it silently. During the tournament it picked up every knockout round with no manual changes.
- **`clean.py`** flattens the JSON into Power BI-ready CSVs: player_match, player_totals, team_match, shots, standings, matches, players and teams. It also derives own goals, results and goal margins, and adds flag URLs for all 48 nations. Files are written as plain UTF-8, because a byte-order mark (BOM) breaks Power BI's header detection.
- **`refresh.py`** runs snapshot → clean → flags and stops with a clear message if any step fails.

> **Honest note:** the phase 3 scripts currently run from a separate working folder next to this repo and are not yet committed here. This repo holds the phase 1 SQL and cleaning work and the phase 2 FBref scripts. Bringing the phase 3 pipeline into the repo is the next clean-up step.

### Data model

| Table | Grain | Rows |
|---|---|---|
| `matches` | one per match | 104 |
| `team_match` | one per team per match | 208 |
| `player_match` | one per player per match | 5,324 |
| `player_totals` | exactly one per player | 1,248 |
| `shots` | one per shot | 2,633 |
| `players`, `teams` | reference, with flag URLs | 1,258 / 48 |
| `standings` | group stage only | 48 |

There are ten many-to-one, single-direction relationships, and the fact tables link to `matches`, `teams` and `players` directly. An earlier design tried to filter shots through `team_match`, but that path does not exist. A match slicer then showed identical totals for every match, and adding direct `match_id` relationships fixed it.

### Own goals: why there are two goal totals

The shot map credits an own goal to the team that **benefits** from it, but no player gets the goal. So for each team in each match:

```
own_goals = max(0, non-shoot-out shot-map goals − sum of player goals)
goals     = player goals + own_goals
```

xG is deliberately left unchanged, because an own goal is not the team's shot, and counting it would fake finishing over-performance. As a result, two correct totals exist side by side: **294** player-credited goals (Overview KPI) and **308** team goals (team-level visuals). The difference is the **14** own goals.

Other rules applied everywhere:

- Shoot-out kicks are excluded from all goal and xG calculations.
- `home_score`/`away_score` are regulation plus extra time, while `winner` includes shoot-outs.
- Extra time is real data, so the xG race axis runs to the last minute played (120+).

---

## Dashboards (Power BI)

**1. Overview** (built)
- KPI band: matches, goals, goals per match, top keeper and top scorer, both with FIFA-style tiebreaks.
- Hero: team xG vs goals scatter, with a diagonal reference line showing over- and under-performers.
- "Where goals come from": a tournament shot map plotted on a penalty-box overlay image aligned to the shot coordinates.
- "When goals are scored": goals vs xG by 15-minute band.

**2. Matchups** (built)
- Pick any match and the whole page recalculates.
- Hero: a cumulative xG race between the two teams.
- Also on the page: a KPI table (shots, possession, big chances, fouls) and a goalscorers list (minute, scorer, situation).
- The data does not link an assist to a specific goal, so the list deliberately shows scorer and situation only.

**3. Attack** and **4. Defence** are scoped but not built yet; see [docs/dashboard_plan_attack_defence.md](docs/dashboard_plan_attack_defence.md). The planned order is Overview → Attack → Defence → Matchups. Position-based pages were rejected because they would present team results, such as clean sheets, as individual performance.

The report theme is in `PowerBI/wc2026_theme.json`.

## SQL analyses (phase 1, MySQL)

| File | Question |
|---|---|
| `01_team_win_rates.sql` | All-time win rate for each FIFA member with 30+ matches |
| `02_goals_per_tournament.sql` | Total goals in each World Cup edition |
| `03_form_last_10.sql` | Win rate over each team's last 10 matches |
| `04_head_to_head.sql` | Head-to-head record between two teams |
| `05_wc_goals_per_game.sql` | Which World Cup had the highest goals per game |
| `06_home_vs_away_advantage.sql` | How much home advantage affects win rates |
| `fifa_teams.sql` | Reference table of the 211 FIFA member associations, used to filter the queries above |

Results exported for Tableau are in `Exports/`.

---

## Limitations

- **Phase 3 code is not in this repo yet** (see the note above). The scripts here also use hard-coded Windows paths and need editing before they run elsewhere.
- **No tracking data.** Distance, sprints or work-rate analysis is impossible, and the project does not fake it from event data.
- **No assist-to-goal link.** Assist totals exist, but which pass set up which goal is unknown.
- **`is_outside_box` from the API is broken** (True for almost every shot). Shot zones are computed from x/y coordinates instead.
- **Standings are group stage only**, so knockout totals are checked against the shot map and player stats instead.
- **Shot-stopping is limited.** If the API's `xg_against` is pre-shot xG (likely), it cannot measure goalkeeping quality (that would need post-shot xG). The Defence page will use save % and say so.
- **Raw defensive counts** (tackles, clearances) make teams under heavy pressure look busy rather than good. They will be shown with that caveat.
- **Phase 2 data is frozen** at the point FBref stopped serving advanced stats.
- `fifa_teams.sql` names were written to match the results dataset, but its own header asks you to run the included check query first.

## How to run

**Historical SQL (phase 1).** You need MySQL and Python with `pandas` and `mysql-connector-python`.
1. Update the paths and MySQL credentials in `Notebooks/clean_historical_results.py`, then run it. It cleans `Data/Raw/results.csv` and loads the `wc2026` database.
2. Run `SQL/fifa_teams.sql`, then the numbered queries in order.

**FBref scripts (phase 2, archived).** `Notebooks/refresh_data.py` scrapes with `soccerdata`, and the football-data.org step runs only if `FOOTBALL_DATA_TOKEN` is set in `.env`. `Notebooks/clean_live_stats.py` builds `Data/Clean/`. Expect the advanced-stats scrape to fail, because FBref no longer serves that data.

**Live pipeline (phase 3).** Put `THESTATSAPI_KEY=<your key>` in a `.env` file. `.env` is git-ignored. Then run `python refresh.py`. After a run, check that player goals + own goals = team goals.

## How it was built

I designed the data model, the metric definitions and every dashboard decision. I direct and debug the code, including with AI assistance, and I understand the logic end to end.
