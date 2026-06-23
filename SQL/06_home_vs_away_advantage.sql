-- ================================================
-- 06_home_vs_away_advantage.sql
-- Question: How much does home advantage affect win rates across all matches?
-- Dataset: wc2026.results (international results 1930-2026)
-- Written: 2026-06-22
-- ================================================
SELECT 'Home' AS perspective,
    COUNT(*) AS total_matches,
    SUM(
        CASE
            WHEN result = 'home_win' THEN 1
            ELSE 0
        END
    ) AS wins,
    SUM(
        CASE
            WHEN result = 'draw' THEN 1
            ELSE 0
        END
    ) AS draws,
    SUM(
        CASE
            WHEN result = 'away_win' THEN 1
            ELSE 0
        END
    ) AS losses,
    ROUND(
        SUM(
            CASE
                WHEN result = 'home_win' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        4
    ) AS win_rate
FROM results
WHERE neutral = 0
UNION ALL
SELECT 'Neutral Venue' AS perspective,
    COUNT(*) AS total_matches,
    SUM(
        CASE
            WHEN result = 'home_win' THEN 1
            ELSE 0
        END
    ) AS wins,
    SUM(
        CASE
            WHEN result = 'draw' THEN 1
            ELSE 0
        END
    ) AS draws,
    SUM(
        CASE
            WHEN result = 'away_win' THEN 1
            ELSE 0
        END
    ) AS losses,
    ROUND(
        SUM(
            CASE
                WHEN result = 'home_win' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        4
    ) AS win_rate
FROM results
WHERE neutral = 1;