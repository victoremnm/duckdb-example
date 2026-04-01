-- Q3 (Advanced): Rank riders by total completed trips within each city
-- Skills: window functions (DENSE_RANK), partitioning, CTEs

WITH rider_trip_counts AS (
    SELECT
        r.rider_id,
        r.city,
        COUNT(t.trip_id) AS total_trips
    FROM riders r
    JOIN trips t ON r.rider_id = t.rider_id
    WHERE t.status = 'completed'
    GROUP BY r.rider_id, r.city
)
SELECT
    city,
    rider_id,
    total_trips,
    DENSE_RANK() OVER (PARTITION BY city ORDER BY total_trips DESC) AS city_rank
FROM rider_trip_counts
ORDER BY city, city_rank;
