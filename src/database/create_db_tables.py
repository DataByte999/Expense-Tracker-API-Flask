from pathlib import Path

import psycopg

from src.config import settings

# Read the SQL file
sql_path = Path("schema.sql")
schema_sql = sql_path.read_text()

# Connect to Postgres
conn = psycopg.connect(settings.db_url)

# Enable autocommit so CREATE TABLE etc. run outside a transaction block
conn.autocommit = True

try:
    with conn.cursor() as cur:
        cur.execute(schema_sql)
    print("Schema applied successfully.")
finally:
    conn.close()
