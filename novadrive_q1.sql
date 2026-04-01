-- Q1 (Warm-up): Total completed trips per vehicle per month
-- Skills: aggregation, date truncation, filtering

SELECT
    vehicle_id,
    DATE_TRUNC('month', start_time::TIMESTAMP) AS trip_month,
    COUNT(*) AS completed_trips
FROM trips
WHERE status = 'completed'
GROUP BY vehicle_id, DATE_TRUNC('month', start_time::TIMESTAMP)
ORDER BY vehicle_id, trip_month;
