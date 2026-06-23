-- ================================================
-- 05_wc_goals_per_game.sql
-- Question: Which World Cup edition had the highest goals per game average?
-- Dataset: wc2026.results (international results 1930-2026)
-- Written: 2026-06-22
-- ================================================
SELECT year,
    COUNT(*) AS total_matches,
    SUM(home_score + away_score) AS total_goals,
    ROUND(SUM(home_score + away_score) / COUNT(*), 2) AS goals_per_game
FROM results
WHERE tournament = 'FIFA World Cup'
GROUP BY year
ORDER BY goals_per_game DESC;