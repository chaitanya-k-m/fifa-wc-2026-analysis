-- Question: How many total goals were scored in each FIFA World Cup edition?
-- Dataset: wc2026.results (international results 1930-2026)
-- Written: 2026-06-22
SELECT year,
    SUM(home_score + away_score) AS total_goals
FROM results
WHERE tournament = 'FIFA World Cup'
GROUP BY year
ORDER BY year;