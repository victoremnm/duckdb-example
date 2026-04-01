"""Load NovaDrive mock CSVs into a persistent DuckDB database."""
import duckdb

DB_PATH = "novadrive.db"

con = duckdb.connect(DB_PATH)

tables = {
    "vehicles": "novadrive_vehicles.csv",
    "riders": "novadrive_riders.csv",
    "trips": "novadrive_trips.csv",
    "sensor_events": "novadrive_sensor_events.csv",
}

for table, csv_file in tables.items():
    con.execute(f"DROP TABLE IF EXISTS {table}")
    con.execute(
        f"CREATE TABLE {table} AS SELECT * FROM read_csv_auto('{csv_file}')"
    )
    count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"  {table}: {count} rows")
    print(con.execute(f"SELECT * FROM {table} LIMIT 3").df().to_string(index=False))
    print()

con.close()
print(f"Database written to {DB_PATH}")
