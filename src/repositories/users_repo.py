import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from src.database.db_connection import get_conn


def insert_user(username: str, email: str, password_hash: str ) -> dict:
    query = """
            INSERT INTO users (username, email, password_hash) 
            VALUES (%s, %s, %s) returning username, email;
            """
    try:
        with get_conn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, (username, email, password_hash))
                new_user = cur.fetchone()
                conn.commit()
                return new_user
    except psycopg.Error as e:
        raise e


def get_user(user_id: int) -> dict | None:
    query = """SELECT username, email FROM users WHERE id = %s"""
    try:
        with get_conn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, (user_id,))
                user_data = cur.fetchone()
                return user_data
    except psycopg.Error as e:
        raise e


def get_user_by_email(email: str) -> dict | None:
    query = """SELECT * FROM users WHERE email = %s"""
    try:
        with get_conn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, (email,))
                user_data = cur.fetchone()
                return user_data
    except psycopg.Error as e:
        raise e


def update_user(user_id: int, data: dict) -> dict | None:
    set_parts = [sql.SQL("{} = %({})s").format(sql.Identifier(col), sql.SQL(col)) for col in data.keys()]
    set_clause = sql.SQL(", ").join(set_parts)
    params = {**data, "user_id": user_id}
    query = sql.SQL("""UPDATE users 
                       SET {set_clause} 
                       WHERE id = %(user_id)s
                       RETURNING username, email;
                    """).format(set_clause=set_clause)
    try:
        with get_conn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, params)
                updated_row = cur.fetchone()
                return updated_row
    except psycopg.Error as e:
        raise e


def delete_user(user_id: int) -> dict | None:
    query = """
            DELETE FROM users WHERE id = (%s) RETURNING username;
            """
    try:
        with get_conn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, (user_id,))
                deleted_row = cur.fetchone()
                return deleted_row
    except psycopg.Error as e:
        raise e
