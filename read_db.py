import duckdb

# Connect to the existing database file in read-only mode
con = duckdb.connect(database='my_database.db', read_only=True)

print(con.execute("SELECT COUNT(*) FROM policies").fetchone())