-- Question: What is the win rate for each FIFA team in their last 10 matches?
-- Dataset: wc2026.results + wc2026.fifa_teams (international results 1930-2026)
-- Written: 2026-06-22
USE wc2026;
WITH all_matches AS (
    SELECT home_team AS team,
        date,
        CASE
            WHEN result = 'home_win' THEN 1
            ELSE 0
        END AS is_win
    FROM results r
        JOIN fifa_teams h ON h.team_name = r.home_team
        JOIN fifa_teams a ON a.team_name = r.away_team
    UNION ALL
    SELECT away_team AS team,
        date,
        CASE
            WHEN result = 'away_win' THEN 1
            ELSE 0
        END AS is_win
    FROM results r
        JOIN fifa_teams h ON h.team_name = r.home_team
        JOIN fifa_teams a ON a.team_name = r.away_team
),
ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY team
            ORDER BY date DESC
        ) AS match_rank
    FROM all_matches
)
SELECT team,
    COUNT(*) AS matches,
    SUM(is_win) AS wins,
    ROUND(SUM(is_win) / COUNT(*), 4) AS form_win_rate
FROM ranked
WHERE match_rank <= 10
GROUP BY team
HAVING COUNT(*) = 10
ORDER BY form_win_rate DESC;