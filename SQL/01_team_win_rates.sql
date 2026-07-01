-- Question: What is the all-time win rate for each FIFA member team with 30+ matches?
-- Dataset: wc2026.results + wc2026.fifa_teams (international results 1930-2026)
-- Written: 2026-06-22
USE wc2026;
SELECT team,
    COUNT(*) AS total_matches,
    SUM(is_win) AS total_wins,
    ROUND(SUM(is_win) / COUNT(*), 4) AS win_rate
FROM (
        SELECT home_team AS team,
            CASE
                WHEN result = 'home_win' THEN 1
                ELSE 0
            END AS is_win
        FROM results r
            JOIN fifa_teams h ON h.team_name = r.home_team
            JOIN fifa_teams a ON a.team_name = r.away_team
        UNION ALL
        SELECT away_team AS team,
            CASE
                WHEN result = 'away_win' THEN 1
                ELSE 0
            END AS is_win
        FROM results r
            JOIN fifa_teams h ON h.team_name = r.home_team
            JOIN fifa_teams a ON a.team_name = r.away_team
    ) AS all_matches
GROUP BY team
HAVING COUNT(*) >= 30
ORDER BY win_rate DESC;