from psycopg import sql
from psycopg.rows import dict_row

from src.database.db_connection import get_conn


def insert_user(username: str, email: str, password_hash: str) -> dict:
    """
    Insert a new user into the database.

    Args:
        username (str): The username of the user.
        email (str): The email of the user.
        password_hash (str): The hashed password of the user.

    Returns:
        dict: Newly inserted username and email.

        {username, email}

    Raises:
        psycopg.errors.Error: If any database-related error occurs during the query execution.
    """
    query = """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s) returning username, email;
            """
    with get_conn() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, (username, email, password_hash))
        conn.commit()
        return cur.fetchone()


def get_user(user_id: int) -> dict | None:
    """
    Retrieve user's data from the database.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: User's username and email.

        None: If no user is found.

    Raises:
        psycopg.errors.Error: If any database-related error occurs during the query execution.
    """
    query = """SELECT username, email FROM users WHERE id = %s"""
    with get_conn() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, (user_id,))
        return cur.fetchone()


def get_user_by_email(email: str) -> dict | None:
    """
    Retrieve user's data by email from the database.

    Args:
        email (str): The email of the user.

    Returns:
        dict: User's id, username, email and hashed password.

        None: If no user is found.

    Raises:
        psycopg.errors.Error: If any database-related error occurs during the query execution.
    """
    query = """SELECT * FROM users WHERE email = %s"""
    with get_conn() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, (email,))
        return cur.fetchone()


def update_user(user_id: int, data: dict) -> dict | None:
    """
    Update user fields in the database.

    Args:
        user_id (int): The ID of the user to update.
        data (dict): Key-value pairs of fields to update.

    Returns:
        dict: Updated user username and email.

        None: If no user is found.

    Raises:
        psycopg.errors.Error: If any database-related error occurs during the query execution.
    """
    set_parts = [
        sql.SQL("{} = %({})s").format(sql.Identifier(col), sql.SQL(col)) for col in data
    ]
    set_clause = sql.SQL(", ").join(set_parts)
    params = {**data, "user_id": user_id}
    query = sql.SQL("""UPDATE users
                       SET {set_clause}
                       WHERE id = %(user_id)s
                       RETURNING username, email;
                    """).format(set_clause=set_clause)
    with get_conn() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, params)
        return cur.fetchone()


def delete_user(user_id: int) -> dict | None:
    """
    Delete a user from the database.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        dict: User's username.

        None: If no user is found.

    Raises:
        psycopg.errors.Error: If any database-related error occurs during the query execution.
    """
    query = """
            DELETE FROM users WHERE id = (%s) RETURNING username;
            """
    with get_conn() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, (user_id,))
        return cur.fetchone()
