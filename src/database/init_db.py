import psycopg
from psycopg import sql
from src.config import settings

# Connect to Postgres (default 'postgres' DB)
conn = psycopg.connect(
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    dbname=settings.DEFAULT_DB_NAME
)

# Enable autocommit so CREATE DATABASE etc. run outside a transaction block
conn.autocommit = True

try:
    with conn.cursor() as cur:
        cur.execute(
            sql.SQL("CREATE DATABASE {};").format(sql.Identifier(settings.DB_NAME))
        )
    print(f"Created database {settings.DB_NAME}")
finally:
    conn.close()
