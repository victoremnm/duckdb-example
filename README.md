# duckdb-example

Practice SQL on realistic datasets — no database server required. Uses [DuckDB](https://duckdb.org/), an in-process analytical database that runs SQL directly on CSV files.

---

## Quick Start (5 minutes)

### 1. Install prerequisites

You need **Python 3.10+** and **uv** (a fast Python package manager):

```shell
# Install uv (if you don't have it)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and install dependencies

```shell
git clone https://github.com/victoremnm/duckdb-example
cd duckdb-example
uv sync
```

### 3. Generate the NovaDrive dataset

```shell
uv run python generate_novadrive_data.py
```

You should see:
```
Generated novadrive_vehicles.csv (50 rows)
Generated novadrive_riders.csv (200 rows)
Generated novadrive_trips.csv (739 rows)
Generated novadrive_sensor_events.csv (833 rows)
Done.
```

### 4. Load into DuckDB

```shell
uv run python create_novadrive_db.py
```

This creates `novadrive.db` with four tables ready to query.

### 5. Run your first query

```shell
uv run python -c "
import duckdb
con = duckdb.connect('novadrive.db')
print(con.execute(open('novadrive_q4.sql').read()).df())
"
```

Expected output:
```
   total_revenue_usd  repeat_rider_revenue_usd  repeat_rider_pct
0           17717.25                  15558.77             87.82
```

---

## NovaDrive Dataset (Interview Practice)

NovaDrive is a fictional autonomous rideshare company. The dataset is designed to mirror the kind of BI questions you'd encounter in a real data analyst interview at an AV company.

### Schema

| Table | Rows | Key columns |
|-------|------|-------------|
| `vehicles` | 50 | `vehicle_id`, `model`, `deployment_date`, `status` (active/retired), `city` |
| `riders` | 200 | `rider_id`, `signup_date`, `city`, `plan_type` (standard/premium) |
| `trips` | ~739 | `trip_id`, `vehicle_id`, `rider_id`, `start_time`, `end_time`, `status` (completed/cancelled/in_progress), `distance_miles`, `fare_usd`, `city` |
| `sensor_events` | ~833 | `event_id`, `vehicle_id`, `event_time`, `event_type`, `severity` |

### SQL Interview Questions

| File | Difficulty | Topic |
|------|-----------|-------|
| `novadrive_q1.sql` | Warm-up | Total completed trips per vehicle per month |
| `novadrive_q2.sql` | Intermediate | Repeat riders joined to vehicle model info |
| `novadrive_q3.sql` | Advanced | City-partitioned rider rankings (`DENSE_RANK`) |
| `novadrive_q4.sql` | Challenging | % of revenue from repeat riders |
| `novadrive_q5.sql` | Niche | Monthly rider cohort retention analysis |

### Run any question

```shell
uv run python -c "
import duckdb
con = duckdb.connect('novadrive.db')
print(con.execute(open('novadrive_q1.sql').read()).df())
"
```

Replace `novadrive_q1.sql` with any question file.

---

## Interactive SQL (DuckDB CLI)

If you want to explore the data interactively:

```shell
duckdb novadrive.db
```

This opens a DuckDB session. Run SQL directly at the `D` prompt:

```
D SHOW TABLES;
D SELECT * FROM trips LIMIT 5;
D SELECT city, COUNT(*) FROM trips GROUP BY city;
D .quit
```

> **Note:** `SELECT`, `SHOW`, and `.quit` are typed *inside* the DuckDB session — they are not shell commands.

---

## Run the Test Suite

```shell
uv sync --group dev     # install pytest (one-time)
uv run pytest tests/ -v
```

17 tests validate data integrity and query correctness.

---

## Original Policy Dataset

The repo also contains an insurance policy churn analysis example (predates the NovaDrive dataset).

| Script | Purpose |
|--------|---------|
| `create_db.py` | Load `mock_data.csv` → `my_database.db` |
| `read_db.py` | Read-only query demo |
| `create_view_question_3.py` | Build churn status view |
| `create_users_table_question_4.py` | Populate users reference table |

SQL questions: `question_1.sql` through `question_4.sql`

---

## Project Structure

```
duckdb-example/
├── generate_novadrive_data.py   # Generate mock CSVs
├── create_novadrive_db.py       # Load CSVs into novadrive.db
├── novadrive_q1.sql             # Interview question 1 (warm-up)
├── novadrive_q2.sql             # Interview question 2 (intermediate)
├── novadrive_q3.sql             # Interview question 3 (advanced)
├── novadrive_q4.sql             # Interview question 4 (challenging)
├── novadrive_q5.sql             # Interview question 5 (cohort retention)
├── tests/
│   └── test_novadrive.py        # Pytest test suite
├── pyproject.toml               # uv project config
└── uv.lock                      # Locked dependency versions
```
