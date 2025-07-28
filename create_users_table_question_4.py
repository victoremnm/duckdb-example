import duckdb

# Assuming 'con' is your DuckDB connection object
con = duckdb.connect(database='my_database.db', read_only=False)

create_users_sql = """
CREATE TABLE IF NOT EXISTS users (
     User_ID VARCHAR,
     Date_of_Birth DATE
 );
"""


con.execute(create_users_sql)
print("Table 'users' created successfully!")

insert_users_sql = """
TRUNCATE users;
 INSERT INTO users (User_ID, Date_of_Birth) VALUES
 ('U001', '1990-05-15'),
 ('U002', '1985-11-22'),
 ('U003', '2000-01-01'),
 ('U004', '1992-07-20'),
 ('U005', '1988-03-10')
"""

con.execute(insert_users_sql)


# Now you can query your new view
result = con.execute("SELECT * FROM users LIMIT 10").fetchdf()
print("\nSample from the new table:")
print(result)

con.close()