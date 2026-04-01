-- Q5 (Niche): Monthly rider cohort retention analysis
-- Cohort = month of rider's first completed trip.
-- Shows what % of each cohort is still taking trips N months later.
-- Skills: date manipulation, multiple CTEs, self-join, window functions

WITH rider_cohorts AS (
    -- Each rider's cohort = month of their first completed trip
    SELECT
        rider_id,
        DATE_TRUNC('month', MIN(start_time::TIMESTAMP)) AS cohort_month
    FROM trips
    WHERE status = 'completed'
    GROUP BY rider_id
),
rider_activity AS (
    -- All (rider, activity_month) combinations for completed trips
    SELECT DISTINCT
        rc.rider_id,
        rc.cohort_month,
        DATE_TRUNC('month', t.start_time::TIMESTAMP) AS activity_month
    FROM rider_cohorts rc
    JOIN trips t ON rc.rider_id = t.rider_id
    WHERE t.status = 'completed'
),
cohort_retention AS (
    SELECT
        cohort_month,
        DATEDIFF('month', cohort_month, activity_month) AS months_since_first_trip,
        COUNT(DISTINCT rider_id) AS active_riders
    FROM rider_activity
    GROUP BY cohort_month, DATEDIFF('month', cohort_month, activity_month)
),
cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT rider_id) AS cohort_size
    FROM rider_cohorts
    GROUP BY cohort_month
)
SELECT
    cr.cohort_month,
    cr.months_since_first_trip,
    cr.active_riders,
    cs.cohort_size,
    ROUND(100.0 * cr.active_riders / cs.cohort_size, 2) AS retention_pct
FROM cohort_retention cr
JOIN cohort_sizes cs ON cr.cohort_month = cs.cohort_month
ORDER BY cr.cohort_month, cr.months_since_first_trip;
