-- ================================================
-- 04_head_to_head.sql
-- Question: What is the head-to-head record between two teams?
-- Dataset: wc2026.results (international results 1930-2026)
-- Written: 2026-06-22
-- ================================================
USE wc2026;
-- Change these two team names to any matchup you want to analyse
SET @team1 = 'Brazil';
SET @team2 = 'Argentina';
SELECT COUNT(*) AS total_matches,
    SUM(
        CASE
            WHEN (
                home_team = @team1
                AND result = 'home_win'
            )
            OR (
                away_team = @team1
                AND result = 'away_win'
            ) THEN 1
            ELSE 0
        END
    ) AS team1_wins,
    SUM(
        CASE
            WHEN result = 'draw' THEN 1
            ELSE 0
        END
    ) AS draws,
    SUM(
        CASE
            WHEN (
                home_team = @team2
                AND result = 'home_win'
            )
            OR (
                away_team = @team2
                AND result = 'away_win'
            ) THEN 1
            ELSE 0
        END
    ) AS team2_wins,
    SUM(
        CASE
            WHEN home_team = @team1 THEN home_score
            ELSE away_score
        END
    ) AS team1_goals,
    SUM(
        CASE
            WHEN home_team = @team2 THEN home_score
            ELSE away_score
        END
    ) AS team2_goals
FROM results
WHERE (
        home_team = @team1
        AND away_team = @team2
    )
    OR (
        home_team = @team2
        AND away_team = @team1
    );