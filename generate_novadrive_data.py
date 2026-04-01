"""Generate NovaDrive mock data CSVs for autonomous rideshare interview practice."""
import csv
import random
from datetime import datetime, timedelta

random.seed(42)

CITIES = ["San Francisco", "Phoenix", "Los Angeles", "Austin", "Seattle"]
VEHICLE_MODELS = ["Jaguar I-PACE", "Chrysler Pacifica", "Zeekr RT"]
VEHICLE_STATUSES = ["active", "active", "active", "retired"]
PLAN_TYPES = ["standard", "premium", "standard", "standard"]
TRIP_STATUSES = ["completed", "completed", "completed", "cancelled", "in_progress"]
EVENT_TYPES = ["sensor_fault", "hard_brake", "lane_departure", "object_detected", "system_alert"]
SEVERITIES = ["low", "low", "medium", "high"]


def rand_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def fmt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def fmt_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


START = datetime(2022, 1, 1)
END = datetime(2024, 12, 31)


# --- Vehicles ---
vehicles = []
for i in range(1, 51):
    deploy = rand_date(datetime(2021, 6, 1), datetime(2023, 1, 1))
    vehicles.append({
        "vehicle_id": f"VH{i:03d}",
        "model": random.choice(VEHICLE_MODELS),
        "deployment_date": fmt_date(deploy),
        "status": random.choice(VEHICLE_STATUSES),
        "city": random.choice(CITIES),
    })

with open("novadrive_vehicles.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["vehicle_id", "model", "deployment_date", "status", "city"])
    w.writeheader()
    w.writerows(vehicles)

print(f"Generated novadrive_vehicles.csv ({len(vehicles)} rows)")


# --- Riders ---
riders = []
for i in range(1, 201):
    signup = rand_date(datetime(2021, 1, 1), datetime(2023, 6, 1))
    city = random.choice(CITIES)
    riders.append({
        "rider_id": f"R{i:04d}",
        "signup_date": fmt_date(signup),
        "city": city,
        "plan_type": random.choice(PLAN_TYPES),
    })

with open("novadrive_riders.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["rider_id", "signup_date", "city", "plan_type"])
    w.writeheader()
    w.writerows(riders)

print(f"Generated novadrive_riders.csv ({len(riders)} rows)")


# --- Trips ---
# ~60% of riders get multiple trips so repeat-rider queries are interesting
trips = []
trip_id = 1
vehicle_ids = [v["vehicle_id"] for v in vehicles]
rider_ids = [r["rider_id"] for r in riders]

for rider_id in rider_ids:
    n_trips = random.choices([1, random.randint(2, 8)], weights=[0.4, 0.6])[0]
    for _ in range(n_trips):
        start = rand_date(START, END - timedelta(hours=2))
        duration_min = random.randint(10, 90)
        end = start + timedelta(minutes=duration_min)
        status = random.choice(TRIP_STATUSES)
        distance = round(random.uniform(1.0, 35.0), 2)
        fare = round(distance * random.uniform(1.5, 3.0), 2)
        trips.append({
            "trip_id": f"T{trip_id:05d}",
            "vehicle_id": random.choice(vehicle_ids),
            "rider_id": rider_id,
            "start_time": fmt(start),
            "end_time": fmt(end) if status != "in_progress" else None,
            "status": status,
            "distance_miles": distance,
            "fare_usd": fare,
            "city": random.choice(CITIES),
        })
        trip_id += 1

with open("novadrive_trips.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=[
        "trip_id", "vehicle_id", "rider_id", "start_time", "end_time",
        "status", "distance_miles", "fare_usd", "city",
    ])
    w.writeheader()
    w.writerows(trips)

print(f"Generated novadrive_trips.csv ({len(trips)} rows)")


# --- Sensor Events ---
events = []
event_id = 1
for v in vehicles:
    n_events = random.randint(10, 30) if v["status"] == "active" else random.randint(1, 8)
    for _ in range(n_events):
        event_time = rand_date(START, END)
        events.append({
            "event_id": f"E{event_id:06d}",
            "vehicle_id": v["vehicle_id"],
            "event_time": fmt(event_time),
            "event_type": random.choice(EVENT_TYPES),
            "severity": random.choice(SEVERITIES),
        })
        event_id += 1

with open("novadrive_sensor_events.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["event_id", "vehicle_id", "event_time", "event_type", "severity"])
    w.writeheader()
    w.writerows(events)

print(f"Generated novadrive_sensor_events.csv ({len(events)} rows)")
print("Done.")
