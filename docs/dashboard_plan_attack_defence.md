# Plan: Dashboard 3 (Attack) and Dashboard 4 (Defence)

Both pages are scoped but not built. The report's planned order is **Overview → Attack → Defence → Matchups**. All measures below use the existing model (`shots`, `team_match`, `player_match`, `player_totals`, `players`, `teams`, `matches`) and its rules:

- Shoot-out kicks (`situation = "shootout"`) are excluded from every goal and xG figure.
- Own goals count for the team that benefits from them.

## Decisions to make before building

| # | Decision | Options | Suggested |
|---|---|---|---|
| 1 | Goals number on the Attack page | 294 player-credited, or 308 team goals including own goals | 294 for player visuals and 308 for team visuals, each labelled |
| 2 | Minimum minutes for per-90 leaderboards | e.g. 270 (three full group matches) | 270, applied to Attack and Defence |
| 3 | Shot threshold for the finishing scatter | about 8 shots | 8 |
| 4 | Is `team_match[xg_against]` pre-shot xG or post-shot (PSxG)? | Check against the opponent's `xg` in the same match | If it equals the opponent's xG, it is pre-shot: use save % and say so |

## Dashboard 3: Attack

**Headline:** *Who scored, who created, who converted?*

| Visual | Fields | Notes |
|---|---|---|
| KPI band | Total goals (decision 1), total xG, top scorer, top assister, penalties scored | Total xG is `SUM(shots[xg])`, excluding shoot-outs. Reuse the Overview **Top Scorer** measure (goals → assists → fewest minutes) |
| **Hero: Golden Boot race** | Top 10 scorers as horizontal bars, in FIFA tiebreak order | Colour bars by goals minus xG (finishing over- or under-performance) |
| Clinical finishers | Scatter: player xG (x) vs goals (y), players with at least 8 shots | Diagonal y = x reference, labelling the outliers |
| Creators | Scatter: xA vs assists, or a key passes + assists per 90 leaderboard | Per-90 values use the decision-2 minutes gate |
| Team attacking output | Scatter: xG per 90 vs goals per 90, one dot per team (48) | Use `team_match` goals, which include own goals |
| Optional: player shot map | Reuse the Overview shot-map overlay with a player slicer | Axis ranges stay fixed at X 15–85, Y −5 to 40 so the image lines up |

New measures, probably on `player_totals` / `player_match` (check what exists first):

```dax
Player xG          = CALCULATE(SUM(shots[xg]), shots[situation] <> "shootout")
Goals minus xG     = [Goals Scored] - [Player xG]
Minutes Played     = SUM(player_match[minutes])
Goals per 90       = DIVIDE([Goals Scored], [Minutes Played]) * 90
Qualifies (270)    = IF([Minutes Played] >= 270, 1, 0)
```

Check the column names against `player_match.csv` before pasting.

**Build in chunks:**
1. KPI band and Golden Boot bars. Check the top scorer against the Overview card (Kylian Mbappé).
2. The two scatters.
3. The team scatter.
4. The optional shot map.

## Dashboard 4: Defence

**Headline:** *Who defended best, and did their goalkeeper make it happen?*

| Visual | Fields | Notes |
|---|---|---|
| **Hero: conceded vs deserved** | Scatter: goals conceded per match (y) vs xG against per match (x), one dot per team | Diagonal = "conceded what you deserved". Teams below the line were saved by their keeper or by luck |
| Golden Glove race | Clean sheets, then total saves as tiebreak, with the minutes gate | Reuse the Overview **Top Keeper** logic, which currently shows Unai Simón |
| Save % leaderboard | `SUM(saves) / SUM(shots on target against)` | Always a ratio of sums, never an average of per-match percentages |
| Defensive workload strip | Tackles + interceptions + clearances per 90, by team | **Caption:** raw defensive counts flatter teams under siege. High workload is not the same as good defending |

**Open data check (decision 4)** comes first. Post-shot xG would support a real shot-stopping metric (PSxG − goals against). Pre-shot xG only supports the conceded-vs-deserved view and save %, and the page should say so.

**Build in chunks:**
1. Run the data check and build the hero scatter.
2. Golden Glove and save %.
3. The workload strip with its caveat caption.

## Out of scope (data does not exist)

- Distance covered, sprints or "work rate": the API has no tracking data.
- Which assist led to which goal: no assist-to-goal link exists.
- `shots[is_outside_box]`: broken in the source. Use the `Shot Zone` column, which is computed from coordinates.
