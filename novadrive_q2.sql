-- Q2 (Intermediate): Repeat riders (2+ trips) with their vehicle model breakdown
-- Skills: multi-table joins, filtering with subqueries/HAVING, aggregation

SELECT
    r.rider_id,
    r.city,
    r.plan_type,
    v.model AS most_used_model,
    COUNT(t.trip_id) AS total_trips,
    ROUND(SUM(t.fare_usd), 2) AS total_fare_usd
FROM riders r
JOIN trips t ON r.rider_id = t.rider_id
JOIN vehicles v ON t.vehicle_id = v.vehicle_id
WHERE t.status = 'completed'
GROUP BY r.rider_id, r.city, r.plan_type, v.model
HAVING COUNT(t.trip_id) >= 2
ORDER BY total_trips DESC;
