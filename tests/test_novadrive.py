"""Unit tests for NovaDrive mock data and SQL interview questions."""
import os
import sys
import pytest
import duckdb

# Ensure repo root is importable and CSVs are found relative to it
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="session")
def con():
    """In-memory DuckDB loaded from the generated CSVs."""
    db = duckdb.connect(":memory:")
    csv_tables = {
        "vehicles": "novadrive_vehicles.csv",
        "riders": "novadrive_riders.csv",
        "trips": "novadrive_trips.csv",
        "sensor_events": "novadrive_sensor_events.csv",
    }
    for table, csv_file in csv_tables.items():
        path = os.path.join(REPO_ROOT, csv_file)
        db.execute(
            f"CREATE TABLE {table} AS SELECT * FROM read_csv_auto('{path}')"
        )
    yield db
    db.close()


def read_sql(filename: str) -> str:
    with open(os.path.join(REPO_ROOT, filename)) as f:
        return f.read()


# ---------------------------------------------------------------------------
# Schema / data integrity
# ---------------------------------------------------------------------------

def test_tables_created(con):
    tables = {r[0] for r in con.execute("SHOW TABLES").fetchall()}
    assert {"vehicles", "riders", "trips", "sensor_events"}.issubset(tables)


def test_row_counts(con):
    assert con.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0] == 50
    assert con.execute("SELECT COUNT(*) FROM riders").fetchone()[0] == 200
    assert con.execute("SELECT COUNT(*) FROM trips").fetchone()[0] > 200
    assert con.execute("SELECT COUNT(*) FROM sensor_events").fetchone()[0] > 100


def test_trip_statuses(con):
    valid = {"completed", "cancelled", "in_progress"}
    statuses = {r[0] for r in con.execute("SELECT DISTINCT status FROM trips").fetchall()}
    assert statuses.issubset(valid)


def test_vehicle_statuses(con):
    valid = {"active", "retired"}
    statuses = {r[0] for r in con.execute("SELECT DISTINCT status FROM vehicles").fetchall()}
    assert statuses.issubset(valid)


def test_no_orphan_trips(con):
    """Every trip references a valid vehicle and rider."""
    orphan_vehicles = con.execute(
        "SELECT COUNT(*) FROM trips t LEFT JOIN vehicles v ON t.vehicle_id = v.vehicle_id WHERE v.vehicle_id IS NULL"
    ).fetchone()[0]
    orphan_riders = con.execute(
        "SELECT COUNT(*) FROM trips t LEFT JOIN riders r ON t.rider_id = r.rider_id WHERE r.rider_id IS NULL"
    ).fetchone()[0]
    assert orphan_vehicles == 0
    assert orphan_riders == 0


# ---------------------------------------------------------------------------
# Q1 — Completed trips per vehicle per month
# ---------------------------------------------------------------------------

def test_q1_returns_rows(con):
    sql = read_sql("novadrive_q1.sql")
    result = con.execute(sql).df()
    assert len(result) > 0
    assert "vehicle_id" in result.columns
    assert "completed_trips" in result.columns


def test_q1_only_completed(con):
    sql = read_sql("novadrive_q1.sql")
    result = con.execute(sql).df()
    assert (result["completed_trips"] > 0).all()


# ---------------------------------------------------------------------------
# Q2 — Repeat riders with vehicle model breakdown
# ---------------------------------------------------------------------------

def test_q2_minimum_two_trips(con):
    sql = read_sql("novadrive_q2.sql")
    result = con.execute(sql).df()
    assert len(result) > 0
    assert (result["total_trips"] >= 2).all()


def test_q2_has_fare_column(con):
    sql = read_sql("novadrive_q2.sql")
    result = con.execute(sql).df()
    assert "total_fare_usd" in result.columns
    assert (result["total_fare_usd"] > 0).all()


# ---------------------------------------------------------------------------
# Q3 — City rankings with DENSE_RANK
# ---------------------------------------------------------------------------

def test_q3_ranks_start_at_one(con):
    sql = read_sql("novadrive_q3.sql")
    result = con.execute(sql).df()
    assert len(result) > 0
    for city, group in result.groupby("city"):
        assert group["city_rank"].min() == 1


def test_q3_ranks_are_dense(con):
    """No gaps in rank values within each city."""
    sql = read_sql("novadrive_q3.sql")
    result = con.execute(sql).df()
    for city, group in result.groupby("city"):
        ranks = sorted(group["city_rank"].unique())
        expected = list(range(1, len(ranks) + 1))
        assert ranks == expected, f"Gap in ranks for city {city}: {ranks}"


# ---------------------------------------------------------------------------
# Q4 — Repeat rider revenue percentage
# ---------------------------------------------------------------------------

def test_q4_single_row(con):
    sql = read_sql("novadrive_q4.sql")
    result = con.execute(sql).df()
    assert len(result) == 1


def test_q4_pct_in_range(con):
    sql = read_sql("novadrive_q4.sql")
    result = con.execute(sql).df()
    pct = result["repeat_rider_pct"].iloc[0]
    assert 0 <= pct <= 100


def test_q4_repeat_revenue_lte_total(con):
    sql = read_sql("novadrive_q4.sql")
    result = con.execute(sql).df()
    assert result["repeat_rider_revenue_usd"].iloc[0] <= result["total_revenue_usd"].iloc[0]


# ---------------------------------------------------------------------------
# Q5 — Cohort retention
# ---------------------------------------------------------------------------

def test_q5_month_zero_is_100(con):
    """Month-0 retention must always be 100%."""
    sql = read_sql("novadrive_q5.sql")
    result = con.execute(sql).df()
    month_zero = result[result["months_since_first_trip"] == 0]
    assert len(month_zero) > 0
    assert (month_zero["retention_pct"] == 100.0).all()


def test_q5_retention_bounded(con):
    sql = read_sql("novadrive_q5.sql")
    result = con.execute(sql).df()
    assert (result["retention_pct"] >= 0).all()
    assert (result["retention_pct"] <= 100).all()


def test_q5_active_riders_lte_cohort_size(con):
    sql = read_sql("novadrive_q5.sql")
    result = con.execute(sql).df()
    assert (result["active_riders"] <= result["cohort_size"]).all()
