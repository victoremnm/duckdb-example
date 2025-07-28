import duckdb

# Connect to a persistent file (or create it)
con = duckdb.connect(database='my_database.db', read_only=False)

# Create a table named 'mock_data_table' from the CSV file
con.execute("CREATE TABLE policies AS SELECT * FROM read_csv_auto('mock_data.csv')")

# Query the persistent table and print the result
results = con.execute("SELECT * FROM policies LIMIT 5").fetchdf()
print(results)