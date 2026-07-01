-- Question: How much does home advantage affect win rates across FIFA matches?
-- Dataset: wc2026.results + wc2026.fifa_teams (international results 1930-2026)
-- Written: 2026-06-22
USE wc2026;
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
FROM results r
    JOIN fifa_teams h ON h.team_name = r.home_team
    JOIN fifa_teams a ON a.team_name = r.away_team
WHERE r.neutral = 0
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
FROM results r
    JOIN fifa_teams h ON h.team_name = r.home_team
    JOIN fifa_teams a ON a.team_name = r.away_team
WHERE r.neutral = 1;