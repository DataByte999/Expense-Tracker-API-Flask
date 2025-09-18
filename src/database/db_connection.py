from psycopg_pool import ConnectionPool
from src.config import settings

# Global connection pool
pool = ConnectionPool(settings.db_url)

def get_conn():
    """Helper function for creating a database connection."""
    return pool.connection()