-- Question: What is the all-time win rate for each team with 30+ matches?
-- Dataset: wc2026.results (international results 1930-2026)
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
        FROM results
        UNION ALL
        SELECT away_team AS team,
            CASE
                WHEN result = 'away_win' THEN 1
                ELSE 0
            END AS is_win
        FROM results
    ) AS all_matches
GROUP BY team
HAVING COUNT(*) >= 30
ORDER BY win_rate DESC;