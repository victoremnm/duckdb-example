-- Q4 (Challenging): Percentage of total fare revenue from repeat riders (2+ trips)
-- Skills: CTEs, conditional aggregation, percentage calculation
-- A "repeat rider" is any rider who has completed at least 2 trips.

WITH rider_trip_counts AS (
    SELECT
        rider_id,
        COUNT(*) AS completed_trips,
        SUM(fare_usd) AS rider_revenue
    FROM trips
    WHERE status = 'completed'
    GROUP BY rider_id
),
revenue_breakdown AS (
    SELECT
        SUM(rider_revenue) AS total_revenue,
        SUM(CASE WHEN completed_trips >= 2 THEN rider_revenue ELSE 0 END) AS repeat_rider_revenue
    FROM rider_trip_counts
)
SELECT
    ROUND(total_revenue, 2) AS total_revenue_usd,
    ROUND(repeat_rider_revenue, 2) AS repeat_rider_revenue_usd,
    ROUND(100.0 * repeat_rider_revenue / total_revenue, 2) AS repeat_rider_pct
FROM revenue_breakdown;
