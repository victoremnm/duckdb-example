# duckdb-example

DuckDB SQL query practice on small CSV datasets — no database server required.

## Setup

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```shell
uv sync
```

For dev dependencies (pytest):

```shell
uv sync --group dev
```

---

## Original Policy Dataset

Demonstrates churn analysis and sales categorization on a mock insurance policy dataset.

| Script | Purpose |
|--------|---------|
| `create_db.py` | Load `mock_data.csv` into `my_database.db` |
| `read_db.py` | Read-only query against `my_database.db` |
| `create_view_question_3.py` | Build `policies_with_churn_status` view |
| `create_users_table_question_4.py` | Populate users reference table |

SQL questions: `question_1.sql` through `question_4.sql`

---

## NovaDrive Interview Prep (Autonomous Rideshare)

Mock data and SQL challenges modeled on BI analyst interview questions for an autonomous vehicle rideshare company.

### Generate data & load DB

```shell
uv run python generate_novadrive_data.py   # creates 4 CSVs
uv run python create_novadrive_db.py        # loads into novadrive.db
```

### SQL Questions

| File | Level | Topic |
|------|-------|-------|
| `novadrive_q1.sql` | Warm-up | Completed trips per vehicle per month |
| `novadrive_q2.sql` | Intermediate | Repeat riders joined to vehicle model |
| `novadrive_q3.sql` | Advanced | City-partitioned rider rankings (DENSE_RANK) |
| `novadrive_q4.sql` | Challenging | % of revenue from repeat riders |
| `novadrive_q5.sql` | Niche | Monthly rider cohort retention analysis |

### Run a query

```shell
uv run python -c "
import duckdb
con = duckdb.connect('novadrive.db')
print(con.execute(open('novadrive_q4.sql').read()).df())
"
```

### Run tests

```shell
uv run pytest tests/ -v
```

### Mock data schema

| Table | Rows (approx) | Key columns |
|-------|--------------|-------------|
| `vehicles` | 50 | vehicle_id, model, deployment_date, status, city |
| `riders` | 200 | rider_id, signup_date, city, plan_type |
| `trips` | ~700 | trip_id, vehicle_id, rider_id, start_time, end_time, status, distance_miles, fare_usd, city |
| `sensor_events` | ~1 000 | event_id, vehicle_id, event_time, event_type, severity |

---

## Interactive DuckDB CLI

```shell
uv run duckdb novadrive.db
SELECT * FROM trips LIMIT 5;
.quit
```
