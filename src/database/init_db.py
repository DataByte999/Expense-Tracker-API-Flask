import psycopg
from psycopg import sql
from src.config import settings

conn = psycopg.connect(
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    dbname=settings.DEFAULT_DB_NAME
)

conn.autocommit = True

with conn.cursor() as cur:
    cur.execute(
        sql.SQL("CREATE DATABASE {};").format(sql.Identifier(settings.DB_NAME))
    )

print(f"Created database {settings.DB_NAME}")

conn.close()