-- ================================================
-- 03_form_last_10.sql
-- Question: What is the win rate for each team in their last 10 matches?
-- Dataset: wc2026.results (international results 1930-2026)
-- Written: 2026-06-22
-- ================================================
with all_matches AS (
    SELECT home_team AS team,
        date,
        CASE
            WHEN result = 'home_win' THEN 1
            ELSE 0
        END AS is_win
    FROM results
    UNION ALL
    SELECT away_team AS team,
        date,
        CASE
            WHEN result = 'away_win' THEN 1
            ELSE 0
        END AS is_win
    FROM results
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