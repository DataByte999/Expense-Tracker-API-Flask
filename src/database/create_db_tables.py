import psycopg
from src.config import settings
from pathlib import Path

# Read the SQL file
sql_path = Path("schema.sql")
schema_sql = sql_path.read_text()

# Connect to Postgres (default 'postgres' DB or whichever you’ve created)
conn = psycopg.connect(
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    dbname=settings.DB_NAME
)

# Enable autocommit so CREATE TABLE etc. run outside a transaction block
conn.autocommit = True

try:
    with conn.cursor() as cur:
        cur.execute(schema_sql)
    print("Schema applied successfully.")
finally:
    conn.close()