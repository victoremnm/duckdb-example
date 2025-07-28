import duckdb

# Assuming 'con' is your DuckDB connection object
con = duckdb.connect(database='my_database.db', read_only=False)
con.execute("CREATE TABLE IF NOT EXISTS policies AS SELECT * FROM 'mock_data.csv'") # Ensure your base table exists

create_view_sql = """
CREATE OR REPLACE VIEW policies_with_churn_status AS
WITH PolicyActivity AS (
    SELECT
        Policy_ID,
        User_ID,
        Created_At,
        Canceled_Date,
        LAG(Canceled_Date) OVER (PARTITION BY User_ID ORDER BY Created_At) AS Previous_Canceled_Date,
        LAG(Created_At) OVER (PARTITION BY User_ID ORDER BY Created_At) AS Previous_Created_At,
        LEAD(Created_At) OVER (PARTITION BY User_ID ORDER BY Created_At) AS Next_Created_At
    FROM policies
),
CalculatedFields AS (
    SELECT
        Policy_ID,
        User_ID,
        Created_At,
        Canceled_Date,
        Previous_Canceled_Date,
        Previous_Created_At,
        Next_Created_At,
        (Previous_Created_At IS NULL OR
         (Previous_Canceled_Date IS NOT NULL AND DATEDIFF('day', Previous_Canceled_Date, Created_At) > 30))
        AS is_new_user,
        CASE
            WHEN Canceled_Date IS NULL THEN NULL
            WHEN Next_Created_At IS NOT NULL AND DATEDIFF('day', Canceled_Date, Next_Created_At) <= 30 THEN NULL
            ELSE Canceled_Date + INTERVAL '30 day'
        END AS Churned_Date
    FROM PolicyActivity
)
SELECT
    Policy_ID,
    is_new_user,
    Churned_Date
FROM CalculatedFields;
"""

con.execute(create_view_sql)
print("View 'policies_with_churn_status' created successfully!")

# Now you can query your new view
result = con.execute("SELECT * FROM policies_with_churn_status LIMIT 10").fetchdf()
print("\nSample from the new view:")
print(result)

con.close()