import sys
import subprocess

subprocess.run([sys.executable, '-m', 'pip', 'install', 'duckdb'])
import duckdb

duckdb.read_csv("../mock_data.csv")                # read a CSV file into a Relation
duckdb.sql("SELECT * FROM '../mock_data.csv'")     # directly query a CSV file.quit